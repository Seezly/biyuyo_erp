from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=255)
    business_id = models.ForeignKey('businesses.Business', on_delete=models.CASCADE)
    identification_number = models.CharField(max_length=10)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=16)
    role = models.CharField(max_length=25)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return [self.name, self.email, self.role, self.phone, self.identification_number]
    
    def __bool__(self):
        return self.is_active