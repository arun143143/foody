from django.urls import path
from .views import UserRegistrationView, UserLoginView,VerifyOTPView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup', UserRegistrationView.as_view(), name='signup'),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
    path('login', UserLoginView.as_view(), name='login'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
