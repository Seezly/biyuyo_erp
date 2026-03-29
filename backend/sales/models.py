from django.db import models

# Create your models here.
class Sale(models.Model):
    business_id = models.ForeignKey('businesses.Business', on_delete=models.CASCADE)
    customer_id = models.ForeignKey('customers.Customer', on_delete=models.CASCADE)
    user_id = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    subtotal = models.DecimalField(decimal_places=2)
    discount = models.DecimalField(decimal_places=2)
    tax = models.DecimalField(decimal_places=2)
    total = models.DecimalField(decimal_places=2)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status

    def __float__(self):
        return [self.subtotal, self.discount, self.tax, self.total]

class SaleItem(models.Model):
    sale_id = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product_id = models.ForeignKey('inventory.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(decimal_places=2)
    total_price = models.DecimalField(decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __int__(self):
        return self.quantity
    
    def __float__(self):
        return [self.unit_price, self.total_price]

class Payment(models.Model):
    sale_id = models.ForeignKey(Sale, on_delete=models.CASCADE)
    method = models.CharField(max_length=20)
    amount = models.DecimalField(decimal_places=2)
    reference = models.CharField(max_length=255)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return [self.method, self.status, self.reference]
    
    def __float__(self):
        return self.amount