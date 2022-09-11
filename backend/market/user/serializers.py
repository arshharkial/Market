from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "kind",
        )


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        """
        It creates a user with the given username, email, password, first name, last name, and kind
        :param validated_data: The data that was validated by the serializer
        :return: The user object is being returned.
        """

        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "kind",
        )
        extra_kwargs = {
            "password": {
                "write_only": True,
            },
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            kind=validated_data.get("kind", "buyer"),
        )

        return user


class ChangePasswordSerializer(serializers.Serializer):
    # A serializer for the password change endpoint.
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
