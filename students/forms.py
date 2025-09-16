from django import forms
from .models import Student
from groups.models import Group

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'phone', 'payment', 'group']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500'
            }),
            'payment': forms.NumberInput(attrs={
                'class': 'w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500'
            }),
            # ❌ TextInput emas
            'group': forms.Select(attrs={
                'class': 'w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500'
            }),
        }
