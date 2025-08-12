from django.urls import path
from . import views

app_name = 'categories'

urlpatterns = [
    path('', views.CategoryListCreateView.as_view(), name='category_list_create'),
    path('<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
]
