from rest_framework import serializers
from .models import SalesReport, InventoryReport, FinancialReport


class SalesReportSerializer(serializers.ModelSerializer):
    business_name = serializers.CharField(source='business.name', read_only=True)

    class Meta:
        model = SalesReport
        fields = [
            'id', 'business', 'business_name', 'start_date', 'end_date',
            'total_sales', 'total_items_sold', 'average_sale', 'created_at'
        ]
        read_only_fields = ['business', 'created_at']


class InventoryReportSerializer(serializers.ModelSerializer):
    business_name = serializers.CharField(source='business.name', read_only=True)

    class Meta:
        model = InventoryReport
        fields = [
            'id', 'business', 'business_name', 'total_products', 'total_value',
            'low_stock_count', 'out_of_stock_count', 'report_date', 'created_at'
        ]
        read_only_fields = ['business', 'created_at']


class FinancialReportSerializer(serializers.ModelSerializer):
    business_name = serializers.CharField(source='business.name', read_only=True)

    class Meta:
        model = FinancialReport
        fields = [
            'id', 'business', 'business_name', 'start_date', 'end_date',
            'total_income', 'total_expenses', 'net_profit', 'created_at'
        ]
        read_only_fields = ['business', 'created_at']