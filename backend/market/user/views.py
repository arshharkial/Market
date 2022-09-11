from django.contrib.auth import login
from django.http.response import HttpResponse
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions
from rest_framework.response import Response

# from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, ChangePasswordSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import boto3
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly
from django.shortcuts import render
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model

User = get_user_model()

ses_client = boto3.client("ses", region_name="us-west-2")


# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # LoginLog.objects.create(user=user)
        if request.data.get("user_type", "") == "Influencer":
            user.is_active = False
            user.save()
            ses_client.send_email(
                Source="theadsh99@gmail.com",
                Destination={
                    "BccAddresses": [user.email],
                },
                Message={
                    "Subject": {"Data": "Activate your account", "Charset": "utf-8"},
                    "Body": {
                        "Html": {
                            "Data": render_to_string(
                                "account_activation_email.html",
                                {
                                    "user": user,
                                    "domain": "https://kulaminds.com",
                                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                                    "token": default_token_generator.make_token(user),
                                },
                            ),
                            "Charset": "utf-8",
                        }
                    },
                },
            )
        # return Response({"user": UserSerializer(user, context=self.get_serializer_context()).data, "token": AuthToken.objects.create(user)[1]})
        return Response(
            {"user": UserSerializer(user, context=self.get_serializer_context()).data}
        )


# Login API
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        user = User.objects.filter(username=request.data.get("username", "")).first()
        if not user:
            user = User.objects.filter(email=request.data.get("email", "")).first()
        if user:
            if not user.is_active:
                return Response(
                    {"message": "Please verify your email id"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            else:
                data = {
                    "username": user.username,
                    "password": request.data.get("password"),
                }
                serializer = AuthTokenSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                user = serializer.validated_data["user"]
                login(request, user)
                return super(LoginAPI, self).post(request, format=None)
        else:
            return Response(
                {"message": "Wrong User Credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


# Get User API
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


# Change Password
class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """

    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated successfully",
                "data": [],
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        ses_client.verify_email_identity(EmailAddress=user.username)
        return render(None, "verification_response.html")
    else:
        return HttpResponse("Activation link is invalid")


class UserList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(["POST"])
def resend_verification_email(request):
    email = request.data.get("email", "")
    try:
        user = User.objects.get(username=email)

    except Exception:
        return Response(
            {"detail": "Influencer matching query does not exist"},
            status=status.HTTP_404_NOT_FOUND,
        )

    ses_client.send_email(
        Source="theadsh99@gmail.com",
        Destination={
            "BccAddresses": [user.email],
        },
        Message={
            "Subject": {"Data": "Activate your account", "Charset": "utf-8"},
            "Body": {
                "Html": {
                    "Data": render_to_string(
                        "account_activation_email.html",
                        {
                            "user": user,
                            "domain": "https://kulaminds.com",
                            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                            "token": default_token_generator.make_token(user),
                        },
                    ),
                    "Charset": "utf-8",
                }
            },
        },
    )

    return Response({"detail": "Verification Email Sent"}, status=status.HTTP_200_OK)
