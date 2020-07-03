from django.contrib import admin
from django.urls import path
from .views import  HomeView, ArticleDetailView, AddDocumentView
urlpatterns = [
    path('', HomeView.as_view(), name = 'home'),
    #path('document/', ArticleDetailView.as_view(),name='article-detail'),
    path('document/<int:pk>', ArticleDetailView.as_view(), name = 'article-detail'),
    path('add_doc/', AddDocumentView.as_view(), name = 'add_post')
]