from django import forms
from .models import Santas_list, Kid

class SantasListForm(forms.ModelForm):
    class Meta:
        model = Santas_list
        fields = '__all__'

class KidForm(forms.ModelForm):
    class Meta:
        model = Kid
        fields = ['name', 'niceness_coefficient', 'santas_list', 'wanted_toy']