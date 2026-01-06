from django import forms
from .models import Group

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        # MUHIM O'ZGARTIRISH: students_count olib tashlandi, type va is_active qo'shildi
        fields = ['name', 'teacher', 'type', 'is_active']
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-emerald-500' # Tailwind classlariga mosladim
            }),
            'teacher': forms.Select(attrs={
                'class': 'w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-emerald-500'
            }),
            # YANGI: type maydoni uchun widget
            'type': forms.Select(attrs={
                'class': 'w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-emerald-500'
            }),
            # YANGI: is_active maydoni uchun widget
            'is_active': forms.CheckboxInput(attrs={
                'class': 'rounded border-gray-300 text-emerald-600 shadow-sm focus:ring-emerald-500'
            }),
            
            # Olib tashlangan: students_count
            # 'students_count': forms.NumberInput(...) Kiritilmasligi kerak
        }