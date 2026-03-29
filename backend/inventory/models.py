from django.db import models

# Create your models here.
class Category(models.Model):
    business_id = models.ForeignKey('businesses.Business', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return [self.name, self.description]

class Product(models.Model):
    business_id = models.ForeignKey('businesses.Business', on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    sku = models.CharField(max_length=100)
    cost_price = models.DecimalField(decimal_places=2)
    sell_price = models.DecimalField(decimal_places=2)
    stock = models.IntegerField(null=True, blank=True)
    min_stock = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return [self.name, self.description, self.sku]
    
    def __float__(self):
        return [self.cost_price, self.sell_price]
    
    def __int__(self):
        return [self.stock, self.min_stock]

class InventoryMovement(models.Model):
    business_id = models.ForeignKey('businesses.Business', on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    type = models.CharField(max_length=10)
    quantity = models.IntegerField()
    reference = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

