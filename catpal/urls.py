from django.contrib import admin
from django.urls import path
from .views import  HomeView, ArticleDetailView, AddDocumentView, UpdateDocumentView, DeleteDocumentView
from . import views

urlpatterns = [
    path('', HomeView.as_view(), name = 'home'),
    #path('document/', ArticleDetailView.as_view(),name='article-detail'),
    path('document/<int:pk>', ArticleDetailView.as_view(), name = 'article-detail'),
    path('add_doc/', AddDocumentView.as_view(), name = 'add_post'),
    path('bulk_add_docs/', views.bulk_add_docs, name ="b_add_docs"),
    path('document/edit/<int:pk>', UpdateDocumentView.as_view(), name = 'update_doc'),
    path('document/<int:pk>/remove', DeleteDocumentView.as_view(), name = 'delete_doc')
]