from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .models import Document
from .forms import DocumentForm, EditDocumentForm
from django.urls import reverse_lazy
# Create your views here.


class HomeView(ListView):
    model = Document
    template_name = 'index.html'
    ordering = ['-id'] #for order the list by id descendetly


class ArticleDetailView(DetailView):
    model = Document
    template_name = 'article_detail.html'


class AddDocumentView(CreateView):
    model = Document
    form_class = DocumentForm
    template_name = 'add_doc.html'
    #fields = '__all__'


class UpdateDocumentView(UpdateView):
    model = Document
    form_class = EditDocumentForm
    template_name = 'update.html'
    #fields = ['tags', 'categories']


class DeleteDocumentView(DeleteView):
    model = Document
    template_name = 'delete_doc.html'
    success_url = reverse_lazy('home')

