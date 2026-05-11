from django.db.models import Sum, Count, Avg
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

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

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return SalesReport.objects.all()
        return SalesReport.objects.filter(business_id=user.business_id)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get summary statistics for the business."""
        user = request.user

        if user.is_superuser:
            business_id = request.query_params.get('business_id')
            if business_id:
                businesses = Business.objects.filter(id=business_id)
            else:
                businesses = Business.objects.all()
        else:
            businesses = Business.objects.filter(id=user.business_id)

        summary_data = []
        for business in businesses:
            total_sales = Sale.objects.filter(business=business).aggregate(
                total=Sum('total')
            )['total'] or 0

            total_purchases = Purchase.objects.filter(business=business).aggregate(
                total=Sum('total')
            )['total'] or 0

            total_products = Product.objects.filter(business=business).count()
            low_stock = Product.objects.filter(
                business=business
            ).filter(stock__lt=models.F('min_stock')).count()

            summary_data.append({
                'business_id': business.id,
                'business_name': business.name,
                'total_sales': float(total_sales),
                'total_purchases': float(total_purchases),
                'total_products': total_products,
                'low_stock_count': low_stock,
            })

        return Response(summary_data)

    @action(detail=False, methods=['get'])
    def sales(self, request):
        """Get sales summary."""
        user = request.user

        if user.is_superuser:
            queryset = Sale.objects.all()
        else:
            queryset = Sale.objects.filter(business=user.business_id)

        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__date__lte=end_date)

        total = queryset.aggregate(total=Sum('total'))['total'] or 0
        count = queryset.count()
        avg_sale = total / count if count > 0 else 0

        return Response({
            'total_sales': float(total),
            'count': count,
            'average_sale': float(avg_sale),
        })

    @action(detail=False, methods=['get'])
    def inventory(self, request):
        """Get inventory summary."""
        user = request.user

        if user.is_superuser:
            queryset = Product.objects.all()
        else:
            queryset = Product.objects.filter(business=user.business_id)

        total_products = queryset.count()
        total_value = queryset.aggregate(
            total=Sum(models.F('stock') * models.F('cost_price'))
        )['total'] or 0
        low_stock = queryset.filter(stock__lt=models.F('min_stock')).count()
        out_of_stock = queryset.filter(stock=0).count()

        return Response({
            'total_products': total_products,
            'total_value': float(total_value),
            'low_stock_count': low_stock,
            'out_of_stock_count': out_of_stock,
        })

    @action(detail=False, methods=['get'])
    def customers(self, request):
        """Get customers summary."""
        from customers.models import Customer
        user = request.user

        if user.is_superuser:
            queryset = Customer.objects.all()
        else:
            queryset = Customer.objects.filter(business=user.business_id)

        total = queryset.count()
        with_sales = queryset.annotate(
            sale_count=Count('sale')
        ).filter(sale_count__gt=0).count()

        return Response({
            'total_customers': total,
            'customers_with_sales': with_sales,
        })

    @action(detail=False, methods=['get'])
    def global_stats(self, request):
        """
        Get global statistics for admin dashboard.
        Only accessible by superusers.
        """
        # Check if user is superuser
        if not request.user.is_superuser:
            return Response(
                {'detail': 'Not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Import models needed for the query
        from accounts.models import CustomUser
        from billing.models import Subscription
        
        # Get total businesses
        total_businesses = Business.objects.count()
        
        # Get total users
        total_users = CustomUser.objects.count()
        
        # Get total sales (sum of all sale totals)
        total_sales = Sale.objects.aggregate(
            total=Sum('total')
        )['total'] or 0
        
        # Get active subscriptions count
        active_subscriptions = Subscription.objects.filter(
            status='active'
        ).count()
        
        return Response({
            'totalBusinesses': total_businesses,
            'totalUsers': total_users,
            'totalSales': float(total_sales),
            'activeSubscriptions': active_subscriptions,
        })


from django.db import models