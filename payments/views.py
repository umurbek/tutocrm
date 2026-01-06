# payments/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Payment
from .forms import PaymentForm # payments/forms.py dan
from students.models import Student
from django.db.models import Q

# -------------------------------------------------------------
# 📋 To'lovlar ro'yxati (Barcha to'lovlar, filtrlash)
# -------------------------------------------------------------
@login_required
def payment_list_view(request):
    # Faqat Boss yoki Admin ko'rishi mumkin
    if not request.user.is_boss and not request.user.is_superuser:
        messages.error(request, "Sizda to'lovlar ro'yxatini ko'rish uchun ruxsat yo'q.")
        return redirect('dashboard:index') # Agar 'dashboard:index' URL mavjud bo'lmasa, uni 'students:student_list' ga o'zgartiring

    payments_query = Payment.objects.all().select_related('student__user', 'student__group')
    
    # Qidiruv / Filtr mantig'i (Masalan, status bo'yicha)
    status_filter = request.GET.get('status')
    if status_filter:
        payments_query = payments_query.filter(status=status_filter)
        
    # Muddati o'tgan to'lovlarni tekshirish (modelning check_overdue metodi chaqirilishi kerak bo'lishi mumkin)
    # Lekin hozircha faqat holatni shablon uchun belgilab qo'yamiz.
    payments_list = []
    today = timezone.now().date()
    for payment in payments_query.order_by('-due_date'):
        if payment.status == 'pending' and payment.due_date < today:
            payment.is_overdue_today = True # Shablon uchun qo'shimcha xossa
        payments_list.append(payment)
        
    context = {
        'payments': payments_list,
        'status_filter': status_filter,
        'status_choices': Payment.STATUS_CHOICES
    }
    return render(request, 'payments/payment_list.html', context)

# -------------------------------------------------------------
# ➕ Yangi To'lov Yaratish (Faqat Boss/Admin)
# -------------------------------------------------------------
@login_required
def payment_create_view(request):
    if not request.user.is_boss and not request.user.is_superuser:
        messages.error(request, "Sizda to'lov qo'shish uchun ruxsat yo'q.")
        return redirect('payments:payment_list')

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            
            # Agar status 'completed' bo'lsa, payment_date ni avtomatik belgilash
            if payment.status == 'completed' and not payment.payment_date:
                payment.payment_date = timezone.now()
            
            payment.save()
            
            messages.success(request, f"O'quvchi {payment.student.user.get_full_name()} uchun {payment.amount} so'm to'lov qo'shildi.")
            return redirect('payments:payment_list')
    else:
        form = PaymentForm()
        
    return render(request, 'payments/payment_form.html', {'form': form})