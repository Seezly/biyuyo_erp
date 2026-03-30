from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUserManager(BaseUserManager):
    """Custom user manager to handle user creation and superuser creation using email instead of username

    Args:
        BaseUserManager (BaseUserManager): Django's built-in user manager
    """

    def create_user(
        self,
        first_name,
        last_name,
        email,
        business_id,
        identification_number,
        phone,
        role,
        password,
        **extra_fields
    ):
        """Custom user creation method to create a user using email instead of username

        Args:
            first_name (string): user's first name
            last_name (string): user's last name
            email (string): user email address
            business_id (integer): business ID to which the user belongs
            identification_number (string): User unique identification number
            phone (string): User phone number
            role (string): User role
            password (string): User password

        Raises:
            ValueError: if any required field is not provided

        Returns:
            CustomUser: returns the created user
        """
        if not first_name:
            raise ValueError("The First Name field must be set")
        if not last_name:
            raise ValueError("The Last Name field must be set")
        if not email:
            raise ValueError("The Email field must be set")
        if not business_id:
            raise ValueError("The Business ID field must be set")
        if not identification_number:
            raise ValueError("The Identification Number field must be set")
        if not phone:
            raise ValueError("The Phone field must be set")
        if not role:
            raise ValueError("The Role field must be set")

        email = self.normalize_email(email)
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            business_id=business_id,
            identification_number=identification_number,
            phone=phone,
            role=role,
            **extra_fields
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(
        self,
        first_name,
        last_name,
        email,
        business_id,
        identification_number,
        phone,
        role,
        password,
        **extra_fields
    ):
        """Custom superuser creation method

        Args:
            email (email): user email address
            business_id (integer): business ID to which the user belongs
            identification_number (string): User unique identification number
            phone (string): User phone number
            role (string): User role
            password (string): User password

        Raises:
            ValueError: if the user is not set as staff or superuser
            ValueError: if the user role is not set to superadmin

        Returns:
            CustomUser: the created superuser
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        if role != "superadmin":
            raise ValueError("Superuser must have role='superadmin'.")

        return self.create_user(
            first_name,
            last_name,
            email,
            business_id,
            identification_number,
            phone,
            role,
            password,
            **extra_fields
        )


class CustomUser(AbstractUser):
    """Custom User Model to override username usable logic for User creation

    Args:
        AbstractUser: Django's built-in AbstractUser model
    """

    username = None
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    business_id = models.ForeignKey("businesses.Business", on_delete=models.CASCADE)
    identification_number = models.CharField(max_length=10, unique=True)
    phone = models.CharField(max_length=16, unique=True)
    role = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "business_id",
        "identification_number",
        "phone",
        "role",
    ]

    objects = CustomUserManager()

    def __str__(self):
        return [
            self.first_name,
            self.last_name,
            self.email,
            self.role,
            self.phone,
            self.identification_number,
        ]

    def __bool__(self):
        return self.is_active
