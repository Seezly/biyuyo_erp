from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=255)
    business_id = models.ForeignKey('businesses.Business', on_delete=models.CASCADE)
    phone = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return [self.name, self.phone]