# students/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, Avg, Sum # Count, Avg, Sum qo'shildi

from django.utils import timezone
from datetime import timedelta

# Model importlari
from .models import Student
from .forms import StudentForm
from tasks.models import TaskAssignment # Vazifa modeli kerak
from payments.models import Payment # To'lov modeli kerak

# -------------------------------------------------------------
# 👁️ O'quvchi Detal Sahifasi
# -------------------------------------------------------------
@login_required
def student_detail_view(request, pk):
    # Student profilini yuklash, kerakli bog'liqliklar bilan
    student = get_object_or_404(
        Student.objects.select_related('user', 'group__teacher__user'), 
        pk=pk
    )
    user = request.user
    
    # Ruxsat cheklovi: Boss, Admin yoki studentning guruh o'qituvchisi
    can_view = (
        user.is_boss or 
        user.is_superuser or 
        (hasattr(user, 'is_teacher') and user.is_teacher and student.group and hasattr(student.group, 'teacher') and student.group.teacher.user == user)
    )

    if not can_view:
        messages.error(request, "Siz bu o'quvchi ma'lumotlarini ko'rish uchun ruxsatga ega emassiz.")
        return redirect('students:student_list')

    # --- 1. Vazifalar Statistikasi ---
    task_stats = {
        'total_tasks': 0,
        'completed_tasks': 0,
        'pending_review': 0,
        'overdue_tasks': 0,
        'average_score': 0.0,
        'last_5_submissions': []
    }
    
    # TaskAssignment modelining mavjudligini tekshirish va guruh mavjudligini tekshirish
    if 'TaskAssignment' in globals() and student.group:
        all_assignments = TaskAssignment.objects.filter(student=student)
        
        task_stats['total_tasks'] = all_assignments.count()
        task_stats['completed_tasks'] = all_assignments.filter(is_completed=True).count()
        
        # Tekshiruv kutilayotganlar: bajarilgan, lekin feedback bo'sh
        task_stats['pending_review'] = all_assignments.filter(
            is_completed=True, feedback=""
        ).count()
        
        # Muddati o'tgan, lekin bajarilmaganlar
        task_stats['overdue_tasks'] = all_assignments.filter(
            is_completed=False, 
            task__due_date__lt=timezone.now().date()
        ).count()
        
        # O'rtacha baho (score maydoni mavjudligini tekshirish)
        if hasattr(TaskAssignment, 'score'):
            avg_score_result = all_assignments.filter(is_completed=True, score__isnull=False).aggregate(Avg('score'))
            task_stats['average_score'] = round(avg_score_result['score__avg'] or 0.0, 1)
        else:
            task_stats['average_score'] = 0.0 # Score maydoni yo'q, 0.0 qilib qo'yamiz

        # Oxirgi 5 ta topshirilgan vazifa 
        # XATO TUZATILDI: '-submission_date' o'rniga '-completed_at' ishlatildi
        task_stats['last_5_submissions'] = all_assignments.filter(is_completed=True).order_by('-completed_at').select_related('task')[:5]

    # --- 2. To'lov Statistikasi ---
    payment_stats = {
        'last_payment_date': 'Noma\'lum',
        'upcoming_due_date': 'Mavjud emas',
        'is_in_debt': 'Yo\'q',
    }
    
    if 'Payment' in globals():
        last_payment = Payment.objects.filter(student=student, status='completed').order_by('-payment_date').first()
        if last_payment:
            payment_stats['last_payment_date'] = last_payment.payment_date.strftime("%Y-%m-%d")

        upcoming_payment = Payment.objects.filter(student=student, status='pending', due_date__gte=timezone.now().date()).order_by('due_date').first()
        if upcoming_payment:
            payment_stats['upcoming_due_date'] = upcoming_payment.due_date.strftime("%Y-%m-%d")
            
        overdue_pending_payments = Payment.objects.filter(student=student, status='pending', due_date__lt=timezone.now().date()).exists()
        
        # Student modelidagi current_debt xossasidan foydalanish afzal
        # Eslatma: Agar 'student.is_in_debt' xossasi mavjud bo'lmasa, bu qismni o'zgartirish kerak bo'ladi.
        if student.is_in_debt: 
            payment_stats['is_in_debt'] = 'Ha'
        else:
             payment_stats['is_in_debt'] = 'Yo\'q'


    context = {
        'student': student,
        'task_stats': task_stats,
        'payment_stats': payment_stats,
        'group': student.group,
        'teacher': student.group.teacher if student.group and student.group.teacher else None
    }
    
    return render(request, 'students/student_detail.html', context)


# -------------------------------------------------------------
# 📋 O'quvchilar ro'yxati (Filtrlash va Qidiruv mantig'i)
# -------------------------------------------------------------
@login_required
def student_list(request):
    user = request.user
    
    # Optimizatsiya: kerakli bog'liqliklar oldindan yuklab olinadi
    students_query = Student.objects.all().select_related('user', 'group', 'group__teacher') 
    
    # 1. ROLGA ASOSLANGAN FILTR (TEACHER)
    if hasattr(user, 'is_teacher') and user.is_teacher:
        # O'qituvchiga faqat o'zi dars beradigan guruhlardagi o'quvchilarni ko'rsatish
        students_query = students_query.filter(group__teacher__user=user)
        
    # 2. QIDIRUV MANTIG'I
    search_query = request.GET.get('q') # URL dan 'q' parametrini olamiz
    
    if search_query:
        # CustomUser'ga bog'langan maydonlar bo'yicha qidiruv (ism, familiya, email, telefon)
        query = (
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(user__email__icontains=search_query) |
            Q(user__phone__icontains=search_query)
        )
        students_query = students_query.filter(query)

    students = students_query.order_by('-join_date')
    
    context = {
        'students': students,
        'search_query': search_query # Shablonga qaytarish
    }
    return render(request, 'students/student_list.html', context)

# -------------------------------------------------------------
# ➕ O'quvchi qo'shish (Faqat Admin/Boss ga ruxsat)
# -------------------------------------------------------------
@login_required
def student_create(request):
    # Faqat Boss yoki Superuserga ruxsat beriladi
    if not request.user.is_boss and not request.user.is_superuser:
        messages.error(request, "Sizda o'quvchi qo'shish uchun ruxsat yo'q. Faqat Boshliq/Admin qo'sha oladi.")
        return redirect('students:student_list') 
        
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Yangi o'quvchi muvaffaqiyatli qo'shildi.")
            return redirect('students:student_list')
    else:
        form = StudentForm()
    return render(request, 'students/student_form.html', {'form': form})

# -------------------------------------------------------------
# ✏️ O'quvchini tahrirlash (Ruxsat cheklovlari mavjud)
# -------------------------------------------------------------
@login_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    user = request.user

    # Ruxsat cheklovi: Boss/Admin yoki studentning guruh o'qituvchisi
    can_edit = (
        user.is_boss or 
        user.is_superuser or 
        (hasattr(user, 'is_teacher') and user.is_teacher and student.group and hasattr(student.group, 'teacher') and student.group.teacher.user == user)
    )

    if not can_edit:
        messages.error(request, "Siz bu o'quvchini tahrirlash uchun ruxsatga ega emassiz.")
        return redirect('students:student_list')

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, f"{student.user.get_full_name()} ma'lumotlari tahrirlandi.")
            return redirect('students:student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/student_form.html', {'form': form})

# -------------------------------------------------------------
# 🗑️ O'quvchini o'chirish (Faqat Boss/Admin)
# -------------------------------------------------------------
@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    
    # Faqat Boss yoki Superuserga ruxsat beriladi
    if not request.user.is_boss and not request.user.is_superuser:
        messages.error(request, "Sizda o'quvchini o'chirish uchun ruxsat yo'q.")
        return redirect('students:student_list')

    if request.method == 'POST':
        student_name = student.user.get_full_name()
        student.delete()
        messages.success(request, f"O'quvchi '{student_name}' o'chirildi.")
        return redirect('students:student_list')
    
    return render(request, 'students/student_confirm_delete.html', {'student': student})