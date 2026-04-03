from django.apps import apps
from django.db import models


# Create your models here.
class Business(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    rif = models.CharField(max_length=10, unique=True)
    address = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    municipality = models.CharField(max_length=255)
    phone = models.CharField(max_length=16, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def __bool__(self):
        return self.is_active

    def get_owner(self):
        User = apps.get_model("accounts", "User")
        return User.objects.filter(business_id=self.id, role="owner").first()

    def get_users(self):
        User = apps.get_model("accounts", "User")
        return User.objects.filter(business_id=self.id)

    def get_customers(self):
        Customer = apps.get_model("customers", "Customer")
        return Customer.objects.filter(business_id=self.id)

    def get_suppliers(self):
        Supplier = apps.get_model("suppliers", "Supplier")
        return Supplier.objects.filter(business_id=self.id)
