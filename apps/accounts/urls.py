from django.urls import path
from .views import RegisterView, LoginView, LogoutView, MeView, AdminLoginView, AdminRegisterView

urlpatterns = [
    # Customer Auth
    path('register/', RegisterView.as_view(), name='auth-register'),
    path('login/', LoginView.as_view(), name='auth-login'),
    
    # Admin Auth
    path('admin/login/', AdminLoginView.as_view(), name='auth-admin-login'),
    path('admin/register/', AdminRegisterView.as_view(), name='auth-admin-register'),
    
    # Session / User Profile
    path('logout/', LogoutView.as_view(), name='auth-logout'),
    path('me/', MeView.as_view(), name='auth-me'),
]

