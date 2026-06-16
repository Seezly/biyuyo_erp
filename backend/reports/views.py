from django.db import models
from django.db.models import Sum, Count
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from businesses.models import Business
from sales.models import Sale
from inventory.models import Product
from suppliers.models import Purchase

from .models import SalesReport, InventoryReport, FinancialReport
from .serializers import (
    SalesReportSerializer,
    InventoryReportSerializer,
    FinancialReportSerializer,
)


class ReportViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for generating and retrieving reports.
    """

    serializer_class = SalesReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        business = self.get_business_filter()
        if business:
            return SalesReport.objects.filter(business_id=business)
        return SalesReport.objects.all()

    def get_business_filter(self):
        if self.request.impersonated:
            return self.request.business
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='admin').exists():
            return None
        return self.request.business

    @action(detail=False, methods=["get"])
    def summary(self, request):
        """Get summary statistics for the business."""
        business = request.business

        total_sales = (
            Sale.objects.filter(business_id=business).aggregate(total=Sum("total"))[
                "total"
            ]
            or 0
        )

        total_purchases = (
            Purchase.objects.filter(business_id=business).aggregate(
                total=Sum("total")
            )["total"]
            or 0
        )

        total_products = Product.objects.filter(business_id=business).count()
        low_stock = (
            Product.objects.filter(
                business_id=business,
                stock__isnull=False,
                min_stock__isnull=False,
            )
            .filter(stock__lt=models.F("min_stock"))
            .count()
        )

        return Response([
            {
                "business_id": business.id,
                "business_name": business.name,
                "total_sales": float(total_sales),
                "total_purchases": float(total_purchases),
                "total_products": total_products,
                "low_stock_count": low_stock,
            }
        ])

    @action(detail=False, methods=["get"])
    def sales(self, request):
        """Get sales summary."""
        queryset = Sale.objects.filter(business_id=request.business)

        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__date__lte=end_date)

        total = queryset.aggregate(total=Sum("total"))["total"] or 0
        count = queryset.count()
        avg_sale = total / count if count > 0 else 0

        return Response(
            {
                "total_sales": float(total),
                "count": count,
                "average_sale": float(avg_sale),
            }
        )

    @action(detail=False, methods=["get"])
    def inventory(self, request):
        """Get inventory summary."""
        queryset = Product.objects.filter(business_id=request.business)

        total_products = queryset.count()
        total_value = (
            queryset.aggregate(total=Sum(models.F("stock") * models.F("cost_price")))[
                "total"
            ]
            or 0
        )
        low_stock = (
            queryset.filter(
                stock__isnull=False,
                min_stock__isnull=False,
            )
            .filter(stock__lt=models.F("min_stock"))
            .count()
        )
        out_of_stock = queryset.filter(stock=0).count()

        return Response(
            {
                "total_products": total_products,
                "total_value": float(total_value),
                "low_stock_count": low_stock,
                "out_of_stock_count": out_of_stock,
            }
        )

    @action(detail=False, methods=["get"])
    def customers(self, request):
        """Get customers summary."""
        from customers.models import Customer

        queryset = Customer.objects.filter(business_id=request.business)

        total = queryset.count()
        with_sales = (
            queryset.annotate(sale_count=Count("sale")).filter(sale_count__gt=0).count()
        )

        return Response(
            {
                "total_customers": total,
                "customers_with_sales": with_sales,
            }
        )

    @action(detail=False, methods=["get"])
    def global_stats(self, request):
        """
        Get global statistics for admin dashboard.
        Only accessible by superusers.
        """
        if not request.user.is_superuser:
            return Response(
                {"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN
            )

        from accounts.models import CustomUser
        from billing.models import Subscription

        total_businesses = Business.objects.count()
        total_users = CustomUser.objects.count()
        total_sales = Sale.objects.aggregate(total=Sum("total"))["total"] or 0
        active_subscriptions = Subscription.objects.filter(status="active").count()

        return Response(
            {
                "totalBusinesses": total_businesses,
                "totalUsers": total_users,
                "totalSales": float(total_sales),
                "activeSubscriptions": active_subscriptions,
            }
        )
