from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # User registration and profile
    path('register/', views.UserRegistrationView.as_view(), name='user_register'),
    path('me/', views.UserProfileView.as_view(), name='user_profile'),
    
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('change-password/', views.change_password_view, name='change_password'),
]
