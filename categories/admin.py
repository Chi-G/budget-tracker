from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for the Category model.
    """
    list_display = ['name', 'description', 'transaction_count', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'description']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']

    def transaction_count(self, obj):
        """Display the number of transactions in this category."""
        return obj.transactions.count()
    
    transaction_count.short_description = 'Transaction Count'
