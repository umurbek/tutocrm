# payments/forms.py

from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['student', 'amount', 'due_date', 'payment_date', 'status', 'notes']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'border rounded px-3 py-2 w-full'}),
            'payment_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'border rounded px-3 py-2 w-full'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'border rounded px-3 py-2 w-full'}),
        }
        labels = {
            'student': 'O\'quvchi',
            'amount': 'Miqdori',
            'due_date': 'To\'lov muddati',
            'payment_date': 'To\'lov qilingan sana',
            'status': 'Holati',
            'notes': 'Izohlar',
        }