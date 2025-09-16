from django import forms
from .models import DashboardStat, MonthlyExpense


class DashboardStatsForm(forms.ModelForm):
    class Meta:
        model = DashboardStat
        fields = ["new_students", "total_students", "graduated_students", "conversion_rate"]
        widgets = {
            "new_students": forms.NumberInput(attrs={"class": "w-full border rounded-lg px-3 py-2"}),
            "total_students": forms.NumberInput(attrs={"class": "w-full border rounded-lg px-3 py-2"}),
            "graduated_students": forms.NumberInput(attrs={"class": "w-full border rounded-lg px-3 py-2"}),
            "conversion_rate": forms.NumberInput(attrs={"class": "w-full border rounded-lg px-3 py-2", "step": "0.1"}),
        }


class MonthlyExpenseForm(forms.ModelForm):
    class Meta:
        model = MonthlyExpense
        fields = ["month", "amount", "category"]
        widgets = {
            "month": forms.TextInput(attrs={"class": "w-full border rounded-lg px-3 py-2"}),
            "amount": forms.NumberInput(attrs={"class": "w-full border rounded-lg px-3 py-2"}),
            "category": forms.Select(attrs={"class": "w-full border rounded-lg px-3 py-2"}),
        }
