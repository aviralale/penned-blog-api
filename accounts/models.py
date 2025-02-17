from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, email, name='', bio='', password=None, **extra_fields):
        """
        Creates and saves a User with the given username, email, and password.
        """
        if not username:
            raise ValueError('Users must have a username.')
        if not email:
            raise ValueError('Users must have an email address.')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, name = name, bio = bio, **extra_fields)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, username,name,bio, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given username, email, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username=username, name=name, bio=bio, email=email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model for the application.
    """
    email = models.EmailField(verbose_name="Email Address", unique=True, max_length=254)
    username = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=66, blank=True) 
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False) 
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'  # Field used for login
    REQUIRED_FIELDS = ['email']  # Additional fields required during user creation

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        """
        Check if the user has a specific permission.
        """
        return True  # All users have permissions by default

    def has_module_perms(self, app_label):
        """
        Check if the user has permissions to view the app `app_label`.
        """
        return True  # All users have module-level permissions by default

    @property
    def is_admin_user(self):
        """
        Check if the user is an admin.
        """
        return self.is_admin or self.is_superuser