from rest_framework import serializers
from .models import Transaction
from categories.serializers import CategorySerializer


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for Transaction model with detailed category information.
    """
    category_detail = CategorySerializer(source='category', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id', 'amount', 'type', 'category', 'category_detail', 
            'date', 'description', 'user_username', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user_username', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Set the user from the request context
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class TransactionCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating transactions (minimal fields).
    """
    class Meta:
        model = Transaction
        fields = ['amount', 'type', 'category', 'date', 'description']

    def create(self, validated_data):
        # Set the user from the request context
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class TransactionSummarySerializer(serializers.Serializer):
    """
    Serializer for transaction summary data.
    """
    total_income = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_expenses = serializers.DecimalField(max_digits=10, decimal_places=2)
    net_balance = serializers.DecimalField(max_digits=10, decimal_places=2)
    transaction_count = serializers.IntegerField()
    income_count = serializers.IntegerField()
    expense_count = serializers.IntegerField()
    category_breakdown = serializers.DictField()
