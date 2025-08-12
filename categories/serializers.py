from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model.
    """
    transaction_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'transaction_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'transaction_count']

    def get_transaction_count(self, obj):
        """Get the number of transactions in this category."""
        return obj.transactions.count()


class CategoryCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating categories (minimal fields).
    """
    class Meta:
        model = Category
        fields = ['name', 'description']
