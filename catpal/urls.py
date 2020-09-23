from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name = 'home'),
    path('home/', views.HomeView.as_view(), name = 'home'),
    path('groups/', views.user_groups , name='groups'),
    path('groups/<group_id>/', views.group_documents, name='group_documents'),
    path('admin_groups/', views.admin_groups, name='admin_groups'),
    path('admin_groups/<group_id>/', views.admin_group_details, name='admin_group_details'),
    path('admin_users/', views.admin_users, name='admin_users'),
    path('admin_users/<user_id>/', views.admin_user_details, name='admin_user_details'),
    path('admin_add_group/', views.admin_add_group, name='admin_add_group'),


    #path('document/', ArticleDetailView.as_view(),name='article-detail'),
    path('document/<int:pk>/', views.ArticleDetailView.as_view(), name = 'article-detail'),
    path('add_doc/', views.AddDocumentView.as_view(), name = 'add_post'),
    path('bulk_add_docs/', views.bulk_add_docs, name ="bulk_add_docs"),
    path('bulk_add_cats/', views.bulk_add_cats, name='bulk_add_cats'),
    path('document/edit/<int:pk>/', views.UpdateDocumentView.as_view(), name = 'update_doc'),
    path('document/<int:pk>/remove', views.DeleteDocumentView.as_view(), name = 'delete_doc'),


]