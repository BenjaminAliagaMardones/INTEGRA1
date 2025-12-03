from django import forms
from .models import Company, Cooperative


class CompanyForm(forms.ModelForm):
    """Formulario para crear/editar empresas"""
    class Meta:
        model = Company
        fields = ['name', 'sector', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Mi PYME Tecnológica'}),
            'sector': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe tu empresa...'}),
        }


class CooperativeForm(forms.ModelForm):
    """Formulario para crear/editar cooperativas"""
    class Meta:
        model = Cooperative
        fields = ['name', 'sector', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Cooperativa Tech Chile'}),
            'sector': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe la cooperativa...'}),
        }
