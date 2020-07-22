from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .models import Document
from .forms import DocumentForm, EditDocumentForm
from django.urls import reverse_lazy
from catpal.models import Document
import json
from .Mendeley import mendeley_driver as md
from .Mendeley import clasify_run as clf
# Create your views here.


class HomeView(ListView):
    model = Document
    template_name = 'index.html'
    ordering = ['-id'] #for order the list by id descendetly

    def get_context_data(self, *, object_list=None, **kwargs):
        cats = clf.generate_categories_visualization_values()
        cat2 = [('----' * cat[1]) + cat[0] for cat in cats]


        context = super(HomeView, self).get_context_data(**kwargs)
        context.update({"cat_list": cat2 })
        return context


class ArticleDetailView(DetailView):
    model = Document
    template_name = 'article_detail.html'

    with open('C:/Users/Jomz/PycharmProjects/catpalsite/catpal/to_clasify_21-07-2020_14-02-24.json') as fp:
        data = json.load(fp)
        print(data)

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context.update({'cat_list': self.data})
        return context

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


def bulk_add_docs(request):
    """
    with open('C:/Users/Jomz/PycharmProjects/catpalsite/catpal/to_clasify_21-07-2020_14-02-24.json') as fp:
        data = json.load(fp)
        print (data)

    printable = "sas"
    """

    data = md.get_documents_to_clasify()
    errors = ""
    for doc in data:
        doc_temp = Document(id_mendeley=doc.id, title = doc.title , abstract = doc.abstract)
        try:
            doc_temp.save()
        except Exception as e:
            errors = errors + "\n" + str(e)




    return render(request, 'bulk_add_docs.html', {"var": "s", "errors": errors})


