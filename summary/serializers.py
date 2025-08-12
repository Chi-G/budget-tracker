from rest_framework import serializers
from decimal import Decimal


class SummarySerializer(serializers.Serializer):
    """
    Serializer for financial summary data.
    """
    total_income = serializers.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_expenses = serializers.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    net_balance = serializers.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    transaction_count = serializers.IntegerField(default=0)
    income_count = serializers.IntegerField(default=0)
    expense_count = serializers.IntegerField(default=0)
    category_breakdown = serializers.DictField(default=dict)


class CategoryBreakdownSerializer(serializers.Serializer):
    """
    Serializer for category-wise spending breakdown.
    """
    category_name = serializers.CharField()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    transaction_count = serializers.IntegerField()
    transaction_type = serializers.CharField()
