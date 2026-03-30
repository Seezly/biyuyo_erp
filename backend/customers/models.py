from django.db import models


# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=255)
    business_id = models.ForeignKey("businesses.Business", on_delete=models.CASCADE)
    phone = models.CharField(max_length=16)
    identification_number = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["business_id", "identification_number"],
                name="unique_customer_identification_number",
            ),
            models.UniqueConstraint(
                fields=["business_id", "phone"], name="unique_customer_phone"
            ),
        ]

    def __str__(self):
        return self.name
