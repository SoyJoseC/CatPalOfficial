from django.contrib import admin
from django.urls import path
from .views import UserRegisterView,PasswordsChangeView, UserEditView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name = 'register'),
    path('edit_profile/', UserEditView.as_view(), name = 'edit_profile'),
    #path('password/', auth_views.PasswordChangeView.as_view(template_name= 'registration/change-password.html')),
    path('password/', PasswordsChangeView.as_view(template_name= 'registration/change-password.html'), name = 'password_change'),
    path('pasword_success/', views.password_success, name = 'password_success'),
    ]