from django import forms
from .models import Teacher

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'email', 'phone', 'subject']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-indigo-500'}),
            'email': forms.EmailInput(attrs={'class': 'w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-indigo-500'}),
            'phone': forms.TextInput(attrs={'class': 'w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-indigo-500'}),
            'subject': forms.TextInput(attrs={'class': 'w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-indigo-500'}),
        }
