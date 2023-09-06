from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import EmailActivateTokenCheckView, LoginView, SignUpView

urlpatterns = [
    path("api/auth/login", LoginView.as_view(), name="user_login"),
    path("api/auth/signup", SignUpView.as_view(), name="user_signup"),
    path(
        "api/auth/activate/<identifier>/<token>",
        EmailActivateTokenCheckView.as_view(),
        name="activate_account",
    ),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
