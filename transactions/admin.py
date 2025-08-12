from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """
    Admin interface for the Transaction model.
    """
    list_display = ['user', 'amount', 'type', 'category', 'date', 'description_short', 'created_at']
    list_filter = ['type', 'category', 'date', 'created_at']
    search_fields = ['user__username', 'description', 'category__name']
    ordering = ['-date', '-created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Transaction Details', {
            'fields': ('user', 'amount', 'type', 'category', 'date', 'description')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def description_short(self, obj):
        """Display a shortened version of the description."""
        if obj.description:
            return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
        return '-'
    
    description_short.short_description = 'Description'
