from django.contrib import admin
from .models import MonthlyExpense

@admin.register(MonthlyExpense)
class MonthlyExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'month', 'amount')
    list_filter = ('user',)

