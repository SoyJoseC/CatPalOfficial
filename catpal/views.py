from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.utils.datastructures import MultiValueDictKeyError
from django.urls import reverse_lazy

from .forms import DocumentForm, EditDocumentForm
from catpal.models import Document, Category, MendeleyGroup
from  members.models import User

# mendeley imports
from .Mendeley import mendeley_driver as md


# Cambios para correr offline sin mendeley
# HomeView
# bulk_add_docs
# bulk_add_cats



class HomeView(ListView):
    model = Document
    template_name = 'index.html'
    ordering = ['-id'] #for order the list by id descendetly

    def get_context_data(self, *, object_list=None, **kwargs):
        # cambios para funcionar offline
        # data de prueba
        cat2 = ['home', '---- lab', '--------microscope', '----hitchen']

        # cats = clf.generate_categories_visualization_values()
        # cat2 = [('----' * cat[1]) + cat[0] for cat in cats]


        context = super(HomeView, self).get_context_data(**kwargs)
        context.update({"cat_list": cat2 })
        return context


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
    # fields = ['tags', 'categories']
    """
    def get_context_data(self, **kwargs):
        data = Category.objects.all.order_by('name')
        context = super(UpdateDocumentView, self).get_context_data(**kwargs)
        context.update({'cat_list': data})
        return context
    """


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
    data = []
    # data = md.get_documents_to_clasify()

    estado = "Documents added succesfully"
    errors = ""
    for doc in data:
        doc_temp = Document(id_mendeley=doc.id, title = doc.title , abstract = doc.abstract)
        try:
            doc_temp.save()
        except Exception as e:
            estado = "ERROR"
            errors = errors + "\n" + str(e)

    return render(request, 'bulk_add_docs.html', {"estado": estado, "errors": errors})


def bulk_add_cats(request):
    # data de prueba
    cats = [('cat1', 0), ('cat2', 1)]

    # modificado para correr offline
    # cats = clf.generate_categories_visualization_values()
    errors = ""
    estado = "Categories added succesfully"
    for elem in cats:
        cat_temp = Category(name=elem[0])
        try:
            cat_temp.save()
        except Exception as e:
            estado = "ERROR"
            errors = errors + '\n' + str(e)

    return render(request, 'bulk_add_categories.html', {"errors": errors, "estado": estado})


def group_details(request, group_id):
    if request.user.is_authenticated:
        group = MendeleyGroup.objects.get(mendeley_id=group_id)
        return render(request, 'group_details.html', {'group': group})
    else:
        return HttpResponseForbidden()


def user_groups(request):
    # get only the user groups
    groups = request.user.groups.all()
    return render(request, 'user_groups.html', {'groups': groups})


def group_documents(request, group_id):
    context = {}
    group = MendeleyGroup.objects.get(mendeley_id=group_id)
    context['group'] = group
    # Get the documents that belongs to the group.
    documents = group.documents.all()
    context['documents'] = documents
    return render(request, 'group_documents.html', context)


# *************************************Staff Views**********************************************

def admin_groups(request):
    if request.user.is_staff and request.user.is_staff:
        groups = MendeleyGroup.objects.all()
        return render(request, 'admin_groups.html', {'groups': groups})
    else:
        return HttpResponseForbidden()


def admin_group_details(request, group_id):
    if request.user.is_staff and request.user.is_staff:
        context = {}
        group = MendeleyGroup.objects.get(mendeley_id=group_id)
        context['group'] = group

        if request.method == 'GET':
            return render(request, 'admin_group_details.html', context)

        elif request.method == 'POST':
            if request.POST['action'] == 'syncfrommendeley':
                # Search for the documents in the group
                md.authenticate(group.mendeley_username, group.mendeley_password)
                mendeley_docs = md.get_documents_of_group(group_id)
                # for now only check not to have duplicates.
                for mendeley_doc in mendeley_docs:
                    try:
                        # if the document exist in the database
                        doc = Document.objects.get(mendeley_id=mendeley_doc.id)
                        doc.title = mendeley_doc.title
                        doc.abstract = mendeley_doc.abstract
                        doc.tags = ', '.join(mendeley_doc.tags)
                        doc.save()
                    except Document.DoesNotExist:
                        # create the document if does not exist in the database
                        doc = Document(
                            mendeley_id = mendeley_doc.id,
                            title = mendeley_doc.title,
                            tags = ', '.join(mendeley_doc.tags),
                            abstract = mendeley_doc.abstract,
                        )
                        doc.save()
                        group.documents.add(doc)
                        pass
                context['sync_changes'] = mendeley_docs
                return render(request, 'admin_group_details.html', context)

            elif request.POST['action'] == 'synctomendeley':
                md.authenticate(group.mendeley_username, group.mendeley_password)
                mendeley_group = md.get_group(group.mendeley_id)
                for doc in group.documents.all():
                    # get the corresponding Mendeley document
                    mendeley_doc = mendeley_group.documents.get(id=doc.mendeley_id, view='all')
                    kwargs = {}
                    if doc.title != mendeley_doc.title:
                        kwargs['title'] = doc.title
                    elif doc.abstract != mendeley_doc.abstract:
                        kwargs['abstract'] = doc.abstract

                    kwargs['tags'] = doc.tags.split(', ')
                    # print(kwargs)
                    # mendeley_doc.update(kwargs)
                    mendeley_doc.update(tags=kwargs['tags'])

                return render(request, 'admin_group_details.html', context)
                pass
            elif request.POST['action'] == 'delete':
                pass
    else:
        return HttpResponseForbidden()


def admin_users(request):
    if request.user.is_staff and request.user.is_staff:
        users = User.objects.all()
        return render(request, 'admin_users.html', {'users': users})
    else:
        return HttpResponseForbidden()


def admin_user_details(request, user_id):
    if request.user.is_staff and request.user.is_staff:
        user = User.objects.get(pk=user_id)
        return render(request, 'admin_user_details.html', {'user': user})
    else:
        return HttpResponseForbidden()


def admin_add_group(request):
    if request.user.is_staff and request.user.is_staff:
        context = {}

        if request.method == 'POST':
            if request.POST['form_id'] == 'user_data':
                mendeley_user = request.POST['mendeley_user']
                mendeley_password = request.POST['mendeley_password']

                # Scan mendeley groups using api.
                try:
                    # login mendeley
                    md.authenticate(mendeley_user, mendeley_password)
                    groups = md.get_groups()
                    context['groups'] = groups
                    context['mendeley_user'] = mendeley_user
                    context['mendeley_password'] = mendeley_password
                except Exception as exc:
                    context['errors'] = [str(exc)]

            elif request.POST['form_id'] == 'groups_data':
                mendeley_user = request.POST['mendeley_user']
                mendeley_password = request.POST['mendeley_password']

                for id, name in request.POST.items():
                    if id == 'form_id' or id == 'csrfmiddlewaretoken' or id == 'mendeley_user' or id == 'mendeley_password':
                        continue
                    # get the group using the ID
                    md.get_group(id)
                    # check if the group exist in the DB
                    try:
                        existing_group = MendeleyGroup.objects.get(mendeley_id=id)
                        # update in the database
                        existing_group.name = name
                        existing_group.mendeley_username = mendeley_user,
                        existing_group.mendeley_password = mendeley_password
                        existing_group.save()
                    except MendeleyGroup.DoesNotExist :
                        # Then create the new object
                        g = MendeleyGroup(
                            mendeley_id=id,
                            name=name,
                            mendeley_username=mendeley_user,
                            mendeley_password=mendeley_password)
                        g.save()

                # redirect to groups view.
                return redirect(to='admin_groups')

        return render(request, 'admin_add_group.html', context)

    else:
        context = {}
        return render(request, 'admin_add_group.html', context)
