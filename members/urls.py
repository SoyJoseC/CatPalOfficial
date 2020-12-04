from django.contrib import admin
from django.urls import path
from .views import UserRegisterView,PasswordsChangeView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name = 'register'),
    #path('password/', auth_views.PasswordChangeView.as_view(template_name= 'registration/change-password.html')),
    path('password/', PasswordsChangeView.as_view(template_name= 'registration/change-password.html'), name = 'password_change'),
    path('pasword_success/', views.password_success, name = 'password_success'),
    ]