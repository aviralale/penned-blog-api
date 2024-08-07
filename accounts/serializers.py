from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from .models import User


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = (
            "id",
            "email",
            "username",
            "password",
            "display_name",
            "profile_pic",
            "bio",
            "gender",
            "date_of_birth",
        )


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = [
            "id",
            "email",
            "username",
            "display_name",
            "profile_pic",
            "bio",
            "gender",
            "date_of_birth",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "is_active",
            "is_admin",
            "is_staff",
            "is_superuser",
            "is_verified",
            "created_at",
            "updated_at",
        ]


class UserProfileSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = [
            "id",
            "email",
            "username",
            "display_name",
            "profile_pic",
            "bio",
            "gender",
            "date_of_birth",
            "is_verified",
        ]
        read_only_fields = ["id", "email", "username", "is_verified"]
