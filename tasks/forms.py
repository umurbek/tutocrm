from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'assigned_teacher', 'group', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full border rounded-lg px-3 py-2'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full border rounded-lg px-3 py-2',
                'rows': 3
            }),
            'due_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full border rounded-lg px-3 py-2'
            }),
            'assigned_teacher': forms.Select(attrs={
                'class': 'w-full border rounded-lg px-3 py-2'
            }),
            'group': forms.Select(attrs={
                'class': 'w-full border rounded-lg px-3 py-2'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full border rounded-lg px-3 py-2'
            }),
        }
