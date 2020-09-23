from django import forms
from catpal.models import Document, Category


class DocumentForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = '__all__'

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
            'categories': forms.CheckboxSelectMultiple(attrs={'class': 'form-checkform-check'}),
            'doc_id': forms.TextInput(attrs={'class': 'form-control'}),
        }
class EditDocumentForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = ['tags', 'categories']

        widgets = {
            #'title': forms.TextInput(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
            'categories': forms.CheckboxSelectMultiple(attrs={'class': 'form-checkform-check'}),
            #'doc_id': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SelectGroupForm(forms.Form):
    groups = ['uno', 'dos']
    widgets = {
        'groups': forms.CheckboxSelectMultiple(attrs={'class': 'form-checkform-check'}),
    }

class JsonBulkAddForm(forms.ModelForm):
    jsonField = forms.Textarea(attrs={'class': 'form-control'})

