# tasks/views.py faylining TUGAL NUXSASI

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.utils import timezone
from django.db import models
# MUHIM MODELLARNI IMPORT QILISH
from students.models import Student  # Talabani topish uchun
from .models import Task, TaskAssignment 
from .forms import TaskForm

# -------------------------------------------------------------
# 📋 Vazifalar ro'yxati (Student uchun filtr qo'shildi)
# -------------------------------------------------------------
@login_required
def task_list(request):
    user = request.user
    tasks_query = Task.objects.all().select_related('target_group', 'created_by')
    student_profile = None # Dastlabki qiymat

    # --- ROLGA ASOSLANGAN FILTR ---

    if hasattr(user, 'is_student') and user.is_student:
        try:
            student_profile = Student.objects.get(user=user, is_active=True)
            
            # Talabaga bevosita tayinlangan barcha TaskAssignment yozuvlarini topish
            assigned_task_ids = TaskAssignment.objects.filter(
                student=student_profile
            ).values_list('task_id', flat=True)
            
            # Talabaga tegishli bo'lgan Task ID'lari orqali filtrlash
            # Va TaskAssignment ma'lumotlarini qo'shimcha annotatsiya orqali yuklash
            tasks_query = tasks_query.filter(id__in=assigned_task_ids)
            
            # 🌟 MUHIM QISM: Talabaning shaxsiy is_completed holatini har bir Task obektiga qo'shish
            tasks_query = tasks_query.annotate(
                # is_completed qiymatini TaskAssignment modelidan olish
                is_assigned_completed=models.Subquery(
                    TaskAssignment.objects.filter(
                        task=models.OuterRef('pk'), # Tashqi Task obyekti PKsi
                        student=student_profile # Yuqorida topilgan Talaba profili
                    ).values('is_completed')[:1] # is_completed maydoni
                )
            )
            
        except Student.DoesNotExist:
            tasks_query = Task.objects.none() 
            messages.warning(request, "Talaba profilingiz topilmadi, vazifalar yuklanmadi.")

    elif hasattr(user, 'is_teacher') and user.is_teacher:
        # O'QITUVCHI UCHUN: O'zi yaratgan yoki o'z guruhlariga tegishli vazifalarni filter qilish
        tasks_query = tasks_query.filter(
            Q(created_by=user) | 
            Q(target_group__teacher__user=user)
        ).distinct()
    
    # Boss yoki Superuser uchun barcha vazifalar ko'rinadi.

    # Vazifalarni muddatiga qarab saralash
    tasks = tasks_query.order_by('-due_date')
    return render(request, 'tasks/task_list.html', {'tasks': tasks})


# -------------------------------------------------------------
# ➕ Vazifa yaratish (Avvalgi kodingiz o'zgarishsiz qoladi)
# -------------------------------------------------------------
@login_required
def task_create(request):
    user = request.user
    
    # Ruxsat cheklovi
    if not (user.is_boss or user.is_superuser or user.is_teacher):
        messages.error(request, "Sizda vazifa yaratishga ruxsat yo'q.")
        return redirect('dashboard:index')

    if request.method == 'POST':
        # Eslatma: TaskForm ichida target_student fieldi mavjud bo'lishi kerak
        form = TaskForm(request.POST, user=user) 
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = user 
            
            task_type = form.cleaned_data['task_type']
            
            # Shaxsiy o'quvchi tayinlangan bo'lsa, Guruhni Null qilish
            if task_type == 'Student':
                task.target_group = None 
            # Guruhga tayinlangan bo'lsa, Shaxsiy o'quvchini Null qilish
            elif task_type == 'Group':
                task.target_student = None
            
            task.save()
            
            # =================================================================
            # ✨ VAZIFA TAYINLASH MANTIQI (TaskAssignment yaratish)
            # =================================================================
            students_to_assign = []

            if task_type == 'Group' and task.target_group:
                # Guruhdagi barcha faol studentlarni topamiz
                students_to_assign = task.target_group.students.filter(is_active=True)
            
            elif task_type == 'Student' and task.target_student:
                 # Faqat bitta shaxsiy o'quvchini qo'shamiz
                 students_to_assign = [task.target_student]

            assignments = []
            for student in students_to_assign:
                assignments.append(
                    TaskAssignment(
                        task=task, 
                        student=student
                    )
                )
            
            if assignments:
                TaskAssignment.objects.bulk_create(assignments)
            # =================================================================

            messages.success(request, "Vazifa muvaffaqiyatli yaratildi va o'quvchilarga tayinlandi.")
            return redirect('tasks:task_list')
    else:
        form = TaskForm(user=user)

    context = {
        'form': form
    }
    return render(request, 'tasks/task_form.html', context)


# -------------------------------------------------------------
# ✏️ Vazifani tahrirlash (update) - O'zgarishsiz
# -------------------------------------------------------------
@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    user = request.user

    # Tahrirlash ruxsatini cheklash
    if not (user.is_boss or user.is_superuser or task.created_by == user):
        messages.error(request, "Siz bu vazifani tahrirlash uchun ruxsatga ega emassiz.")
        return redirect('tasks:task_detail', pk=pk)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user=user) 
        if form.is_valid():
            form.save()
            messages.success(request, f"Vazifa '{task.title}' tahrirlandi.")
            return redirect('tasks:task_detail', pk=pk)
    else:
        form = TaskForm(instance=task, user=user)
    return render(request, 'tasks/task_form.html', {'form': form})
@require_POST
@login_required
def submit_task_assignment(request, task_pk):
    user = request.user
    
    # Faqat Talabalar ruxsat etiladi
    if not (hasattr(user, 'is_student') and user.is_student):
        messages.error(request, "Faqat o'quvchilar vazifani topshirishlari mumkin.")
        return redirect("tasks:task_detail", pk=task_pk)

    try:
        student_profile = Student.objects.get(user=user, is_active=True)
        assignment = TaskAssignment.objects.get(
            task__pk=task_pk, 
            student=student_profile
        )
        
        if not assignment.is_completed:
            assignment.is_completed = True
            assignment.completed_at = timezone.now()
            assignment.save()
            messages.success(request, f"'{assignment.task.title}' vazifasi muvaffaqiyatli topshirildi.")
        else:
            messages.warning(request, "Bu vazifa avvalroq topshirilgan.")
            
    except Student.DoesNotExist:
        messages.error(request, "Talaba profilingiz topilmadi.")
    except TaskAssignment.DoesNotExist:
        messages.error(request, "Sizga bu vazifa tayinlanmagan.")
        
    return redirect("tasks:task_detail", pk=task_pk)

# -------------------------------------------------------------
# ❌ Vazifani o'chirish (delete) - O'zgarishsiz
# -------------------------------------------------------------
@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    user = request.user

    # O'chirish ruxsatini cheklash
    if not (user.is_boss or user.is_superuser or task.created_by == user):
        messages.error(request, "Siz bu vazifani o'chirish uchun ruxsatga ega emassiz.")
        return redirect('tasks:task_detail', pk=pk)
        
    if request.method == 'POST':
        task_title = task.title
        task.delete()
        messages.success(request, f"Vazifa '{task_title}' muvaffaqiyatli o'chirildi.")
        return redirect('tasks:task_list')
    return render(request, 'tasks/task_detail.html', {'task': task, 'confirm_delete': True}) 

# -------------------------------------------------------------
# 🔍 Vazifa detail - O'zgarishsiz
# -------------------------------------------------------------
@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    assignments = task.assignments.all().select_related('student', 'task') 
    
    student_assignment = None
    if hasattr(request.user, 'is_student') and request.user.is_student:
        try:
            # 1. Talaba profilini topish
            student_profile = Student.objects.get(user=request.user, is_active=True)
            # 2. Talabaning shu vazifaga tegishli TaskAssignment yozuvini topish
            student_assignment = TaskAssignment.objects.get(task=task, student=student_profile)
        except (Student.DoesNotExist, TaskAssignment.DoesNotExist):
            student_assignment = None

    return render(request, 'tasks/task_detail.html', {
        'task': task, 
        'assignments': assignments,
        'student_assignment': student_assignment # Contextga qo'shildi
    })
# -------------------------------------------------------------
# ✅ Vazifani bajarilgan deb belgilash (TaskAssignment uchun yangi funksiya kerak)
# -------------------------------------------------------------
@require_POST
@login_required
def task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    
    # Faqat Boss/Teacher/Creator ruxsat etiladi
    if not (request.user.is_superuser or request.user.is_boss or task.created_by == request.user):
        messages.error(request, "Vazifaning umumiy holatini o'zgartirishga ruxsatingiz yo'q.")
        return redirect("tasks:task_detail", pk=pk)
    
    task.status = "done"
    task.save()
    messages.success(request, "Vazifaning umumiy holati Bajarildi deb belgilandi.")
    return redirect("tasks:task_detail", pk=pk)