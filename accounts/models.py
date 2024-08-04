from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from datetime import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, display_name, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        email = self.normalize_email(email)
        user = self.model(
            email=email, display_name=display_name, username=username, **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, display_name, username, password=None, **extra_fields
    ):
        user = self.create_user(
            email, display_name, username, password=password, **extra_fields
        )
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_admin", True)
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_admin") is not True:
            raise ValueError("Superuser must have is_admin=True.")

        return self.create_user(
            email, display_name, username, password=None, **extra_fields
        )


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email",
        max_length=255,
        unique=True,
    )
    display_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    profile_pic = models.ImageField(
        upload_to="user_avatar",
        null=True,
        blank=True,
        default="user_avatar/default/default.jpg",
    )
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]
    bio = models.TextField(max_length=103, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["display_name", "email"]

    def __str__(self):
        return self.username
