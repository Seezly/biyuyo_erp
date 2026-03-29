from django.db import models

# Create your models here.
class Plan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2)
    max_users = models.IntegerField()
    max_products = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def __float__(self):
        return self.price

class Subscription(models.Model):
    business_id = models.ForeignKey("businesses.Business", on_delete=models.CASCADE)
    plan_id = models.ForeignKey("subscriptions.Plan", on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.status

class Invoice(models.Model):
    subscription_id = models.ForeignKey("subscriptions.Subscription", on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2)
    method = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return [self.status, self.method]
    
    def __float__(self):
        return self.amount