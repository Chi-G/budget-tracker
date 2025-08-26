from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from datetime import datetime
from .models import Transaction
from .serializers import TransactionSerializer, TransactionCreateUpdateSerializer


class TransactionListCreateView(generics.ListCreateAPIView):
    """
    View to list user's transactions and create new ones.
    GET: List user's transactions with optional filtering
    POST: Create a new transaction
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type', 'category']

    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user)
        
        # Date range filtering
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
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
        
        return queryset.select_related('category', 'user')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TransactionCreateUpdateSerializer
        return TransactionSerializer


class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a specific transaction.
    GET: Retrieve transaction details
    PUT/PATCH: Update transaction
    DELETE: Delete transaction
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return TransactionCreateUpdateSerializer
        return TransactionSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_filter_view(request):
    """
    Advanced filtering endpoint for transactions.
    GET: Filter transactions by multiple criteria
    """
    queryset = Transaction.objects.filter(user=request.user)
    
    # Filter by transaction type
    transaction_type = request.query_params.get('type')
    if transaction_type in ['income', 'expense']:
        queryset = queryset.filter(type=transaction_type)
    
    # Filter by category
    category_id = request.query_params.get('category')
    if category_id:
        try:
            queryset = queryset.filter(category_id=int(category_id))
        except (ValueError, TypeError):
            pass
    
    # Filter by date range
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
    
    # Search in description
    search = request.query_params.get('search')
    if search:
        queryset = queryset.filter(
            Q(description__icontains=search) | 
            Q(category__name__icontains=search)
        )
    
    # Order by date
    queryset = queryset.select_related('category', 'user').order_by('-date', '-created_at')
    
    serializer = TransactionSerializer(queryset, many=True)
    return Response({
        'count': queryset.count(),
        'results': serializer.data
    })
