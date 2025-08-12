from django.urls import path
from . import views

app_name = 'summary'

urlpatterns = [
    path('', views.financial_summary_view, name='financial_summary'),
    path('categories/', views.category_summary_view, name='category_summary'),
]
