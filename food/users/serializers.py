from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile, OTP

class UserProfileSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=True, max_length=15)

    class Meta: 
        model = UserProfile
        fields = ['phone_number', 'address', 'role']

    def validate_phone_number(self, value):
        """Ensure phone number is unique."""
        if UserProfile.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Phone number already exists.")
        return value

class SignupSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=True, max_length=15)
    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES, required=True)
    email = serializers.EmailField(required=False, allow_blank=True) 

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone_number', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_username(self, value):
        """Ensure username is unique."""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already taken.")
        return value

    def validate_phone_number(self, value):
        """Ensure phone number is unique."""
        if UserProfile.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Phone number already exists.")
        return value

    def validate_email(self, value):
        if UserProfile.objects.filter(email=value).exists():
            raise serializers.ValidationError("email id already exists")
        return value

    def create(self, validated_data):
        phone_number = validated_data.pop('phone_number')
        role = validated_data.pop('role')

        # Create the user
        user = User(username=validated_data['username'], email=validated_data.get('email', ''))
        user.set_password(validated_data['password'])
        user.save()

        # Create the UserProfile with the selected role
        UserProfile.objects.create(user=user, phone_number=phone_number, role=role)
        return user



class OTPRequestSerializer(serializers.Serializer):
    """Serializer for requesting an OTP."""
    phone_number = serializers.CharField(max_length=15)

    def validate_phone_number(self, value):
        """Ensure the phone number is valid (basic check)."""
        if not value.isdigit() or len(value) < 10:
            raise serializers.ValidationError("Invalid phone number.")
        return value

class OTPVerifySerializer(serializers.Serializer):
    """Serializer for verifying OTP."""
    phone_number = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        phone_number = data.get("phone_number")
        otp_code = data.get("otp")

        try:
            otp_entry = OTP.objects.filter(phone_number=phone_number, otp_code=otp_code).latest('created_at')
        except OTP.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP.")

        if otp_entry.is_expired():
            raise serializers.ValidationError("OTP has expired.")

        return data
