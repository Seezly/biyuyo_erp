from django.db import models
from django.utils import timezone


class SalesReport(models.Model):
    business = models.ForeignKey("businesses.Business", on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_items_sold = models.IntegerField(default=0)
    average_sale = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Reporte de ventas - {self.business.name} - {self.start_date} to {self.end_date}"


class InventoryReport(models.Model):
    business = models.ForeignKey("businesses.Business", on_delete=models.CASCADE)
    total_products = models.IntegerField(default=0)
    total_value = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    low_stock_count = models.IntegerField(default=0)
    out_of_stock_count = models.IntegerField(default=0)
    report_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Reporte de inventario - {self.business.name} - {self.report_date}"


class FinancialReport(models.Model):
    business = models.ForeignKey("businesses.Business", on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_income = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total_expenses = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    net_profit = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Reporte financiero - {self.business.name} - {self.start_date} to {self.end_date}"