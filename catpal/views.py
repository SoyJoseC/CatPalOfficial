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


def select_group(request):
    """
    Shows a form with the groups of the User,
    the User will choose one of those groups and the documents of that group will be displayed.
    :param request:
    :return:
    """
    errors = []

    if request.method == 'POST':
        # print(request.POST)
        try:
            group_id = request.POST['selected_group']
            group = MendeleyGroup.objects.get(mendeley_id = group_id)
            # redirect to the group page
            return redirect('group_documents', group_id=group_id)
        except MultiValueDictKeyError:
            # redirect to a message
            errors.append('Debe seleccionar un grupo.')

    groups = MendeleyGroup.objects.all()
    return render(request, 'select_mendeley_group.html', {'groups':groups, 'errors': errors})


def user_groups(request):
    # get only the user groups
    groups = request.user.groups.all()
    return render(request, 'user_mendeley_groups.html', {'groups': groups})


def group_documents(request, group_id):
    print('entre')
    group = MendeleyGroup.objects.get(mendeley_id=group_id)
    # Get the documents that belongs to the group.
    documents = group.documents.all()
    return render(request, 'group_documents.html', {'documents': documents})


# *************************************Staff Views**********************************************

def admin_groups(request):
    if request.user.is_staff and request.user.is_staff:
        groups = MendeleyGroup.objects.all()
        return render(request, 'admin_groups.html', {'groups': groups})
    else:
        return HttpResponseForbidden()


def admin_group_details(request, group_id):
    if request.user.is_staff and request.user.is_staff:
        group = MendeleyGroup.objects.get(mendeley_id=group_id)
        return render(request, 'admin_group_details.html', {'group': group})
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
                        g.save()
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
