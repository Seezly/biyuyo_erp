from django.db import models


# Create your models here.
class Supplier(models.Model):
    name = models.CharField(max_length=255)
    business_id = models.ForeignKey("businesses.Business", on_delete=models.CASCADE)
    rif = models.CharField(max_length=10)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=16)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["business_id", "rif"], name="unique_supplier_rif"
            ),
            models.UniqueConstraint(
                fields=["business_id", "phone"], name="unique_supplier_phone"
            ),
        ]

    def __str__(self):
        return [self.name, self.email, self.address, self.phone, self.rif]

    def __bool__(self):
        return self.is_active


class Purchase(models.Model):
    business_id = models.ForeignKey("businesses.Business", on_delete=models.CASCADE)
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["business_id", "supplier_id", "created_at"],
                name="unique_purchase",
            )
        ]


class PurchaseItem(models.Model):
    purchase_id = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product_id = models.ForeignKey("inventory.Product", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["purchase_id", "product_id"], name="unique_purchase_item"
            )
        ]
