from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
# Students modelini import qilish shart, chunki u Talabaning guruhini aniqlaydi
try:
    from students.models import Student
except ImportError:
    # Agar model topilmasa, istisno bilan ishlash
    Student = None
    messages.error("Group views", "Xato: Student modeli topilmadi. Students app o'rnatilganligiga ishonch hosil qiling.")


from .models import Group
from .forms import GroupForm


# 📋 Guruhlar ro‘yxati (Rolga asoslangan filtr qo'shildi)
@login_required
def group_list(request):
    user = request.user
    
    # 1. Barcha guruhlarni olishni boshlash
    # Faqat aktiv guruhlarni olish tavsiya etiladi
    groups_query = Group.objects.filter(is_active=True).select_related('teacher__user')

    # 2. ROLGA ASOSLANGAN FILTR
    if hasattr(user, 'is_student') and user.is_student and Student:
        # Talaba uchun faqat o'z guruhini ko'rsatish
        try:
            student_profile = Student.objects.get(user=user, is_active=True)
            
            if student_profile.group:
                # Agar talabaning guruhi bo'lsa, faqat shu guruhni ko'rsatish
                groups_query = groups_query.filter(id=student_profile.group.id)
            else:
                # Guruhga a'zo bo'lmagan talaba uchun bo'sh ro'yxat
                groups_query = groups_query.none() 
                
        except Student.DoesNotExist:
            groups_query = groups_query.none()
            messages.warning(request, "Sizning Talaba profilingiz topilmadi.")

    elif hasattr(user, 'is_teacher') and user.is_teacher:
        # O'qituvchi uchun faqat o'zi dars beradigan guruhlarni filter qilish
        groups_query = groups_query.filter(teacher__user=user)
            
    # Boss yoki Superuser uchun groups_query barcha aktiv guruhlarni o'z ichiga oladi.

    # 3. Annotatsiya (Faol talabalar sonini hisoblash)
    groups_query = groups_query.annotate(
        active_students_count=Count('students', filter=Q(students__is_active=True))
    ).order_by('-created_at')


    # 4. Izlash Mantig'i
    search_query = request.GET.get('q') 

    if search_query:
        search_filter = (
            Q(name__icontains=search_query) |  # Yashirin U+00A0 belgisi olib tashlandi
            Q(teacher__user__first_name__icontains=search_query) | 
            Q(teacher__user__last_name__icontains=search_query)
        )
        groups_query = groups_query.filter(search_filter).distinct()
    context = {
        "groups": groups_query,
        "search_query": search_query
    }
    return render(request, "groups/group_list.html", context)


# ➕ Yangi guruh qo‘shish (Boss cheklovi qo'shildi)
@login_required
def group_create(request):
    # Faqat Boss/Superuserga ruxsat berish
    if not request.user.is_boss and not request.user.is_superuser:
        messages.error(request, "Siz guruh qo'shish uchun ruxsatga ega emassiz.")
        return redirect('groups:group_list')
        
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Yangi guruh muvaffaqiyatli qo'shildi!")
            return redirect("groups:group_list")
    else:
        form = GroupForm()
    return render(request, "groups/group_form.html", {"form": form})


# ✏️ Guruhni tahrirlash (Boss cheklovi qo'shildi)
@login_required
def group_update(request, pk):
    group = get_object_or_404(Group, pk=pk)
    
    # Faqat Boss/Superuserga ruxsat berish
    if not request.user.is_boss and not request.user.is_superuser:
        messages.error(request, "Siz bu guruhni tahrirlash uchun ruxsatga ega emassiz.")
        return redirect('groups:group_list')
        
    if request.method == "POST":
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, f"Guruh '{group.name}' muvaffaqiyatli tahrirlandi!")
            return redirect("groups:group_list")
    else:
        form = GroupForm(instance=group)
    return render(request, "groups/group_form.html", {"form": form})


# ❌ Guruhni o‘chirish (Boss cheklovi qo'shildi)
@login_required
def group_delete(request, pk):
    group = get_object_or_404(Group, pk=pk)
    
    # Faqat Boss/Superuserga ruxsat berish
    if not request.user.is_boss and not request.user.is_superuser:
        messages.error(request, "Siz bu guruhni o'chirish uchun ruxsatga ega emassiz.")
        return redirect('groups:group_list')
        
    if request.method == "POST":
        group.delete()
        messages.success(request, f"Guruh '{group.name}' muvaffaqiyatli o'chirildi.")
        return redirect("groups:group_list")
    return render(request, "groups/group_confirm_delete.html", {"group": group})


# 🔍 Guruh detail
@login_required
def group_detail(request, pk):
    group = get_object_or_404(Group, pk=pk)
    
    # Agar talaba o'z guruhidan boshqa guruhni ko'rmoqchi bo'lsa, uni cheklash kerak
    user = request.user
    if hasattr(user, 'is_student') and user.is_student and Student:
        try:
            student_profile = Student.objects.get(user=user, is_active=True)
            if not student_profile.group or student_profile.group.pk != group.pk:
                messages.error(request, "Siz faqat o'z guruh ma'lumotlaringizni ko'rishingiz mumkin.")
                return redirect('groups:group_list')
        except Student.DoesNotExist:
            messages.error(request, "Talaba profilingiz topilmadi.")
            return redirect('groups:group_list')

    return render(request, "groups/group_detail.html", {"group": group})


@login_required
def schedule_view(request):
    context = {}
    return render(request, "groups/schedule.html", context)
def lesson_attendance(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    students = lesson.group.student_set.filter(is_active=True)
    # Bu yerda o'quvchilarni belgilash mantig'i bo'ladi
    return render(request, 'groups/attendance.html', {'lesson': lesson, 'students': students})
