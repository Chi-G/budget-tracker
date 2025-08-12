from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('', views.TransactionListCreateView.as_view(), name='transaction_list_create'),
    path('<int:pk>/', views.TransactionDetailView.as_view(), name='transaction_detail'),
    path('filter/', views.transaction_filter_view, name='transaction_filter'),
]
