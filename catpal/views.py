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
    success_url = reverse_lazy('home')
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


def initial(request):
    from catpal.models import Document
    import json

    #with open ('static/to_clasify_21-07-2020_14-02-24.json', "r") as read_file:
     #   data = json.load(read_file)

    printable = "sas"

    d = Document(title='Creado desde BulkAdd', tags='bulky')
    d.save()



    return render(request, 'initial.html', {"var": printable})

