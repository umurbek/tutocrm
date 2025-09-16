from django import forms
from .models import SystemSettings

class SystemSettingsForm(forms.ModelForm):
    class Meta:
        model = SystemSettings
        fields = ['crm_name', 'language', 'currency', 'logo']
        widgets = {
            'crm_name': forms.TextInput(attrs={'class': 'w-full border rounded-lg px-3 py-2'}),
            'language': forms.Select(attrs={'class': 'w-full border rounded-lg px-3 py-2'}),
            'currency': forms.TextInput(attrs={'class': 'w-full border rounded-lg px-3 py-2'}),
            'logo': forms.FileInput(attrs={
                'class': 'block w-full text-sm text-gray-600 '
                         'file:mr-4 file:py-2 file:px-4 '
                         'file:rounded-lg file:border-0 '
                         'file:text-sm file:font-semibold '
                         'file:bg-indigo-50 file:text-indigo-700 '
                         'hover:file:bg-indigo-100'
            }),
        }
