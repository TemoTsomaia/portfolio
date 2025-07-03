from django import forms
from santas_list.models import Kid
from .models import Toy

class CreateToyForm(forms.Form):
    kid = forms.ModelChoiceField(
        queryset=Kid.objects.filter(niceness_coefficient__gt=5, toy__isnull=True),
        empty_label="Select a Kid",
        label="Select a Kid",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    time_to_create = forms.IntegerField(
        label="Time to Create (in minutes)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        required=True
    )

class AssignForm(forms.Form):
    name = forms.ModelChoiceField(
        queryset=Kid.objects.filter(toy__isnull=True, coal__isnull=True),
        widget=forms.Select(attrs={'class': 'form-control'}),  # Optional: Add styling
        empty_label="Select a Kid",  # The placeholder text for the dropdown
        label="Choose a Kid"
    )