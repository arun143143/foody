from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import SignupSerializer, OTPRequestSerializer
from .models import UserProfile,OTP
from django.contrib.auth.models import User
import random
import requests
from django.core.cache import cache


"""RAPIDAPI_KEY = "1a2a6c2e21msh67e301fc4e850f8p125317jsnae2e35f15de0"."""

RAPIDAPI_KEY ="882567cf02msh4c7fd84fae2c28ep129f30jsnbbc2f5a4c0ea"

class UserRegistrationView(APIView):
    """User Registration API (OTP Verification)"""
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.data.get("phone_number")

        if not phone_number:
            return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Call RapidAPI to send OTP
        url = "https://sms-verify3.p.rapidapi.com/send-numeric-verify"
        payload = {"target": phone_number}
        headers = {
            "x-rapidapi-key": RAPIDAPI_KEY,
            "x-rapidapi-host": "sms-verify3.p.rapidapi.com",
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()

        if response.status_code == 200 and data.get("status") == "success":
            otp = data.get("verify_code")  # Get OTP from response

            # Store OTP in cache for 5 minutes
            cache.set(f"otp_{phone_number}", otp, timeout=300)

            return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)

        return Response({"error": data.get("message", "Failed to send OTP")}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyOTPView(APIView):
    """Verify OTP and Create User"""
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.data.get("phone_number")
        otp_received = request.data.get("otp")

        if not phone_number or not otp_received:
            return Response({"error": "Phone number and OTP are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the OTP from cache
        otp_stored = cache.get(f"otp_{phone_number}")

        if otp_stored and otp_received == otp_stored:

            serializer = SignupSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                cache.delete(f"otp_{phone_number}")  
                return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """User Login API (JWT Token)"""
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Login successful",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "role": user.profile.role
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

