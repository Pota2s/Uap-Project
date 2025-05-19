from django import forms
from . import models

class StoreForm(forms.ModelForm):
    class Meta:
        model = models.Store
        fields = ['name', 'description']