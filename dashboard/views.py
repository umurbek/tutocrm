from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum

from .models import DashboardStat, MonthlyExpense
from students.models import Student   # Student modelini import qildik
from groups.models import Group
from .forms import DashboardStatsForm, MonthlyExpenseForm


# 📊 Dashboard sahifasi (Hamma uchun bitta index.html)
@login_required
def dashboard_view(request):
    # Statistika
    stats = {
        "new_students": Student.objects.count(),
        "total_students": Student.objects.count(),
        "total_groups": Group.objects.count(),  # 🆕 guruhlar soni
        "graduated_students": 0,
        "conversion_rate": 15,
    }

    # Sotuv ma’lumotlari (test)
    sales_labels = ["Yan", "Fev", "Mar", "Apr", "May"]
    sales_data = [1200000, 900000, 1500000, 1800000, 1100000]

    # 🔝 Top 5 student (payment bo‘yicha)
    top_students = Student.objects.order_by('-payment')[:5]

    # 🔝 Top 5 group (talabalar soni bo‘yicha)
    top_groups = Group.objects.order_by('-students_count')[:5]

    context = {
        "stats": stats,
        "sales_labels": sales_labels,
        "sales_data": sales_data,
        "top_students": top_students,
        "top_groups": top_groups,  # 🆕 guruhlar ham qo‘shildi
    }
    return render(request, "dashboard/index.html", context)
# 📥 Statistika qo‘shish (hamma foydalanuvchi uchun)
@login_required
def stats_input_view(request):
    form = DashboardStatsForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        stats = form.save(commit=False)
        stats.user = request.user
        stats.save()
        return redirect('dashboard')
    return render(request, 'dashboard/input.html', {'form': form})


# 💸 Xarajat kiritish (hamma foydalanuvchi uchun)
@login_required
def expense_input_view(request):
    form = MonthlyExpenseForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        expense = form.save(commit=False)
        expense.user = request.user
        expense.save()
        return redirect('dashboard')
    return render(request, 'dashboard/expense_input.html', {'form': form})


# 📈 Umumiy xarajatlar charti (oylar bo‘yicha)
@login_required
def expense_chart_view(request):
    expenses = MonthlyExpense.objects.filter(user=request.user)
    labels = [e.month for e in expenses]
    data = [float(e.amount) for e in expenses]
    return JsonResponse({'labels': labels, 'data': data})


# 🥧 Kategoriya bo‘yicha pie chart
@login_required
def expense_pie_chart_view(request):
    expenses = MonthlyExpense.objects.filter(user=request.user)
    data = expenses.values('category').annotate(total=Sum('amount'))
    return JsonResponse(list(data), safe=False)


# 🕒 Oxirgi 30 kunlik xarajatlar
@login_required
def recent_expense_chart_view(request):
    thirty_days_ago = timezone.now() - timedelta(days=30)
    expenses = MonthlyExpense.objects.filter(
        user=request.user,
        created_at__gte=thirty_days_ago
    )
    data = [{"month": e.month, "amount": float(e.amount)} for e in expenses]
    return JsonResponse(data, safe=False)
