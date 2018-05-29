from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    path = forms.CharField(required=False)
    songfile = forms.FileField(label='Select a music file', help_text='max. 4 megabytes')