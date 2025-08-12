from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count, Q
from decimal import Decimal
from datetime import datetime
from transactions.models import Transaction
from categories.models import Category
from .serializers import SummarySerializer, CategoryBreakdownSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def financial_summary_view(request):
    """
    Get comprehensive financial summary for the authenticated user.
    Includes total income, expenses, balance, and category breakdown.
    """
    user = request.user
    queryset = Transaction.objects.filter(user=user)
    
    # Date range filtering (optional)
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    
    if start_date:
        try:
            start_date = datetime.fromisoformat(start_date)
            queryset = queryset.filter(date__gte=start_date)
        except ValueError:
            pass
            
    if end_date:
        try:
            end_date = datetime.fromisoformat(end_date)
            queryset = queryset.filter(date__lte=end_date)
        except ValueError:
            pass
    
    # Calculate totals
    income_data = queryset.filter(type='income').aggregate(
        total=Sum('amount'),
        count=Count('id')
    )
    expense_data = queryset.filter(type='expense').aggregate(
        total=Sum('amount'),
        count=Count('id')
    )
    
    total_income = income_data['total'] or Decimal('0.00')
    total_expenses = expense_data['total'] or Decimal('0.00')
    net_balance = total_income - total_expenses
    
    # Category breakdown
    category_breakdown = {}
    
    # Income by category
    income_by_category = (
        queryset.filter(type='income')
        .values('category__name')
        .annotate(
            total_amount=Sum('amount'),
            transaction_count=Count('id')
        )
        .order_by('-total_amount')
    )
    
    # Expense by category
    expense_by_category = (
        queryset.filter(type='expense')
        .values('category__name')
        .annotate(
            total_amount=Sum('amount'),
            transaction_count=Count('id')
        )
        .order_by('-total_amount')
    )
    
    category_breakdown['income'] = list(income_by_category)
    category_breakdown['expenses'] = list(expense_by_category)
    
    summary_data = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_balance': net_balance,
        'transaction_count': queryset.count(),
        'income_count': income_data['count'],
        'expense_count': expense_data['count'],
        'category_breakdown': category_breakdown
    }
    
    serializer = SummarySerializer(summary_data)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category_summary_view(request):
    """
    Get spending summary grouped by categories.
    """
    user = request.user
    queryset = Transaction.objects.filter(user=user)
    
    # Optional transaction type filter
    transaction_type = request.query_params.get('type')
    if transaction_type in ['income', 'expense']:
        queryset = queryset.filter(type=transaction_type)
    
    # Date range filtering (optional)
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    
    if start_date:
        try:
            start_date = datetime.fromisoformat(start_date)
            queryset = queryset.filter(date__gte=start_date)
        except ValueError:
            pass
            
    if end_date:
        try:
            end_date = datetime.fromisoformat(end_date)
            queryset = queryset.filter(date__lte=end_date)
        except ValueError:
            pass
    
    # Group by category and transaction type
    category_data = (
        queryset.values('category__name', 'type')
        .annotate(
            total_amount=Sum('amount'),
            transaction_count=Count('id')
        )
        .order_by('category__name', 'type')
    )
    
    # Format the data
    formatted_data = []
    for item in category_data:
        formatted_data.append({
            'category_name': item['category__name'],
            'transaction_type': item['type'],
            'total_amount': item['total_amount'],
            'transaction_count': item['transaction_count']
        })
    
    return Response({
        'count': len(formatted_data),
        'results': formatted_data
    }, status=status.HTTP_200_OK)
