from django import forms
from .models import Group

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'teacher', 'students_count']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500'
            }),
            'teacher': forms.Select(attrs={  # 🔑 dropdown
                'class': 'w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500'
            }),
            'students_count': forms.NumberInput(attrs={
                'class': 'w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500'
            }),
        }
