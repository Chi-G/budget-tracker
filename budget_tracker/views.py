from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class WelcomeView(TemplateView):
    """
    Welcome page for non-authenticated users
    """
    template_name = 'budget_tracker/welcome.html'


class LoginView(TemplateView):
    """
    Login page
    """
    template_name = 'budget_tracker/login.html'


class RegisterView(TemplateView):
    """
    Registration page
    """
    template_name = 'budget_tracker/register.html'


class DashboardView(TemplateView):
    """
    Dashboard page for authenticated users
    """
    template_name = 'budget_tracker/dashboard.html'


class ProfileView(TemplateView):
    """
    User profile page for authenticated users
    """
    template_name = 'budget_tracker/profile.html'
