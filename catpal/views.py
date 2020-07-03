from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView
from .models import Document
# Create your views here.

class HomeView(ListView):
    model = Document
    template_name = 'index.html'


class ArticleDetailView(DetailView):
    model = Document
    template_name = 'article_detail.html'

class AddDocumentView(CreateView):
    model = Document
    template_name = 'add_doc.html'
    fields = '__all__'




