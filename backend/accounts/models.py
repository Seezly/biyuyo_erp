from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.apps import apps


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
        password,
        **extra_fields,
    ):
        """Custom user creation method to create a user using email instead of username

        Args:
            first_name (string): user's first name
            last_name (string): user's last name
            email (string): user email address
            business_id (integer): business ID to which the user belongs
            identification_number (string): User unique identification number
            phone (string): User phone number
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

        email = self.normalize_email(email)
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            business_id=business_id,
            identification_number=identification_number,
            phone=phone,
            **extra_fields,
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(
        self,
        first_name,
        last_name,
        email,
        identification_number,
        phone,
        password,
        **extra_fields,
    ):
        """Custom superuser creation method

        Args:
            first_name (string): user's first name
            last_name (string): user's last name
            email (string): user email address
            identification_number (string): User unique identification number
            phone (string): User phone number
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

        # Get or create a default business for superusers
        Business = apps.get_model("businesses", "Business")
        try:
            business_id = Business.objects.get(pk=1)
        except (Business.DoesNotExist, ValueError):
            business_id = Business.objects.create(
                name="Biyuyo",
                description="Biyuyo Business for staff users",
                rif="J000000000",
                address="N/A",
                state="N/A",
                municipality="N/A",
                phone="04000000000",
                email=email,
            )

        return self.create_user(
            first_name,
            last_name,
            email,
            business_id,
            identification_number,
            phone,
            password,
            **extra_fields,
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "identification_number",
        "phone",
    ]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def __bool__(self):
        return self.is_active
