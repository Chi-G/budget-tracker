from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from decimal import Decimal


User = get_user_model()


class Transaction(models.Model):
    """
    Model to represent financial transactions (income or expenses).
    """
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Transaction amount (must be positive)"
    )
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES, help_text="Income or Expense")
    category = models.ForeignKey(
        'categories.Category', 
        on_delete=models.PROTECT, 
        related_name='transactions',
        help_text="Transaction category"
    )
    date = models.DateTimeField(help_text="Transaction date and time")
    description = models.TextField(blank=True, help_text="Optional transaction description")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['user', 'type']),
            models.Index(fields=['user', 'date']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return f"{self.type.title()}: {self.amount} - {self.category.name} ({self.user.username})"
