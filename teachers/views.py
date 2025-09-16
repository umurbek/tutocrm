from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Teacher
from .forms import TeacherForm

# 👨‍🏫 O‘qituvchilar ro‘yxati
@login_required
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teachers/teacher_list.html', {'teachers': teachers})

# ➕ O‘qituvchi qo‘shish
@login_required
def teacher_create(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teachers:teacher_list')  # 🔥 namespace ishlatilgan
    else:
        form = TeacherForm()
    return render(request, 'teachers/teacher_form.html', {'form': form})

# ✏️ O‘qituvchi yangilash
@login_required
def teacher_update(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('teachers:teacher_list')  # 🔥 namespace ishlatilgan
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'teachers/teacher_form.html', {'form': form})

# ❌ O‘qituvchini o‘chirish
@login_required
def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    teacher.delete()
    return redirect('teachers:teacher_list')  # 🔥 namespace ishlatilgan
