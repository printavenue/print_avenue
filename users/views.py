from typing import Any, List

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from users.backends import EmailPhoneUsernameAuthenticationBackend
from users.models import User
from users.serializers import UserLoginSerializer, UserSerializer
from users.tokens import AccountActivationTokenGenerator

# Create your views here.


class LoginView(GenericAPIView):
    """
    Login to account using username and password.
    username can be:
     - email
     - phone number(including country)
    and password

    if user is not verified, return 401,
    if user is not active, return 403,
    if username or passowrd is not correct, return 401
    if username and password are correct, send:
     - token: access token
     - refresh: refresh token
    """
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]
    authentication_classes: List[Any] = []

    def post(self, request: Request) -> Response:
        seralizer = self.serializer_class(data=request.data)
        seralizer.is_valid(raise_exception=True)
        username = seralizer.validated_data["username"]
        password = seralizer.validated_data["password"]
        user = EmailPhoneUsernameAuthenticationBackend.authenticate(request, username, password)

        if user:
            if not user.is_verified:
                return Response(
                    {"error": 1, "message": "User is not verified."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            if user.is_active:
                token = RefreshToken.for_user(user)
                return Response(
                    {"error": 0, "token": str(token.access_token), "refresh": str(token)},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": 1, "message": "User is not active"}, status=status.HTTP_403_FORBIDDEN
                )
        else:
            return Response(
                {"error": 1, "message": "username or password is not correct."},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class SignUpView(GenericAPIView):
    """
    Register user with phone number or email address
    :body
     - email
     - phone number
     - password

    Raises:
    400 Bad Request: if both email and phone number are empty
    400 Bad Request: if user with the given email exists already

    Send Activation link to user email address
    """
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    authentication_classes: List[Any] = []

    def post(self, request):
        seralizer = self.serializer_class(data=request.data, context={"request": request})
        seralizer.is_valid(raise_exception=True)
        seralizer.save()

        return Response({"error": 0, "message": "Email Activation link is sent to you email."})


class EmailActivateTokenCheckView(GenericAPIView):
    """
    Check validity of password reset token based on user id.

    Required path parameters:
        - uidb64: base64 encoded user id
        - token: password reset token

    Returns success message on valid token, error message on invalid or expired token.
    """

    serializer_class = None
    permission_classes = [AllowAny]
    authentication_classes: List[Any] = []

    def get(self, request: Request, identifier: str, token: str) -> Response:
        try:
            user = User.objects.get(identifier=identifier)

            if not AccountActivationTokenGenerator().check_token(user, token):
                return Response(
                    {"success": False, "message": "Invalid or expired token"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.is_verified = True
            user.save()
            return Response(
                {"success": True, "message": "Account succesfully activated."},
                status=status.HTTP_200_OK,
            )

        except Exception:
            return Response(
                {"success": False, "message": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST,
            )
