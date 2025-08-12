"""
URL configuration for budget_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .views import WelcomeView, LoginView, RegisterView, DashboardView, ProfileView


@api_view(['GET']) 
@permission_classes([AllowAny])
def api_root(request): 
    """
    API root endpoint providing information about available endpoints.
    """
    return Response({
        'message': 'Welcome to Budget Tracker API',
        'version': '1.0.0',
        'endpoints': {
            'auth': {
                'register': '/api/users/register/',
                'login': '/api/auth/login/',
                'logout': '/api/auth/logout/',
                'profile': '/api/users/me/',
            },
            'categories': {
                'list_create': '/api/categories/',
                'detail': '/api/categories/{id}/',
            },
            'transactions': {
                'list_create': '/api/transactions/',
                'detail': '/api/transactions/{id}/',
                'filter': '/api/transactions/filter/',
            },
            'summary': {
                'financial_summary': '/api/summary/',
                'category_summary': '/api/summary/categories/',
            }
        }
    })


urlpatterns = [
    # Frontend Pages
    path('', WelcomeView.as_view(), name='welcome'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('profile/', ProfileView.as_view(), name='profile'),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # API Endpoints
    path('api/', api_root, name='api_root'),
    path('api/users/', include('users.urls')),
    path('api/auth/', include(('users.urls', 'auth'), namespace='auth')),
    path('api/categories/', include('categories.urls')),
    path('api/transactions/', include('transactions.urls')),
    path('api/summary/', include('summary.urls')),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
