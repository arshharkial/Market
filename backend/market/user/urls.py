from django.urls.conf import include
from .views import (
    RegisterAPI,
    LoginAPI,
    UserAPI,
    ChangePasswordView,
    UserDetail,
    UserList,
    activate,
    resend_verification_email,
)
from django.urls import path
from knox import views as knox_views

urlpatterns = [
    path("register/", RegisterAPI.as_view(), name="register"),
    path("login/", LoginAPI.as_view(), name="login"),
    path("logout/", knox_views.LogoutView.as_view(), name="logout"),
    path("logout-all/", knox_views.LogoutAllView.as_view(), name="logoutall"),
    path("user/", UserAPI.as_view(), name="user"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("password_reset/", include("django_rest_passwordreset.urls", namespace="password_reset")),
    path("activate/<uidb64>/<token>", activate, name="activate"),
    path("get-users", UserList.as_view()),
    path("get-users/<int:pk>", UserDetail.as_view()),
    path("resend-verification-email", resend_verification_email, name="resend_verification_email"),
]
