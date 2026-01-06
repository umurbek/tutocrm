from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from django.utils import timezone
from django.db.models import Count, Sum, Avg, Q
from datetime import timedelta, date 

from .models import CustomUser, VerificationCode
from .forms import CustomUserCreationForm, EmailLoginForm

# Modellar importi
from teachers.models import Teacher
from students.models import Student
from groups.models import Group, Lesson # <--- Lesson endi groups.models dan import qilindi

# Task, TaskAssignment va Payment modellarini dinamik import qilish
try:
    # TaskAssignment ham Task bilan birga tasks ilovasida deb faraz qilamiz
    from tasks.models import Task, TaskAssignment 
    from payments.models import Payment
    Submission = None # Submission endi ishlatilmaydi, TaskAssignment ishlatiladi
except ImportError:
    Task, TaskAssignment, Payment = None, None, None 


# =========================
# SIGNUP
# =========================
def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            return redirect("dashboard:index")
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})

# =========================
# PROFILE
# =========================
@login_required
def profile_view(request):
    return render(request, "accounts/profile.html", {"user": request.user})

# =========================
# EMAIL LOGIN
# =========================
def email_login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = None
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, "Bunday email topilmadi.")
            return render(request, "accounts/email_login.html", {"form": EmailLoginForm()})

        # Verification code yaratish
        VerificationCode.objects.filter(user=user).delete()
        vc = VerificationCode.objects.create(user=user)
        vc.generate_code()

        try:
            send_mail(
                "TutorCRM - Tasdiqlash kodi",
                f"Sizning tasdiqlash kodingiz: {vc.code}",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        except Exception as e:
            messages.error(request, f"Email yuborishda xato: {e}")
            return render(request, "accounts/email_login.html", {"form": EmailLoginForm()})

        request.session["pending_user"] = user.id
        return redirect("accounts:verify_code")

    return render(request, "accounts/email_login.html", {"form": EmailLoginForm()})

# =========================
# VERIFY CODE
# =========================
def verify_code_view(request):
    if request.method == "POST":
        code = request.POST.get("code")
        user_id = request.session.get("pending_user")

        if not user_id:
            messages.error(request, "Login jarayoni to‘liq emas.")
            return redirect("accounts:email_login")

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            messages.error(request, "Foydalanuvchi topilmadi.")
            return redirect("accounts:email_login")

        vc = VerificationCode.objects.filter(user=user).last()

        if vc and vc.is_valid() and vc.code == code:
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            request.session.pop("pending_user", None)

            if user.first_login:
                user.first_login = False
                user.save()
                return redirect("accounts:welcome")

            return redirect("dashboard:index")

        messages.error(request, "Kod noto‘g‘ri yoki muddati o‘tgan.")
        return render(request, "accounts/verify_code.html")

    return render(request, "accounts/verify_code.html")

# =========================
# WELCOME
# =========================
@login_required
def welcome_view(request):
    return redirect("dashboard:index")

# =========================
# DASHBOARD
# =========================
@login_required
def dashboard_view(request):
    user = request.user
    context = {'user': user}
    today = timezone.now().date()

    # ---------------- BOSS DASHBOARD ----------------
    if user.is_boss:
        total_teachers = CustomUser.objects.filter(role='teacher', is_active=True).count()
        total_students = CustomUser.objects.filter(role='student', is_active=True).count()
        
        # date_joined CustomUser/AbstractUser maydoni. Bu yer to'g'ri.
        recent_staff = CustomUser.objects.filter(is_active=True).exclude(role='student').order_by('-date_joined')[:5]
        
        total_groups = Group.objects.filter(is_active=True).count() if Group else 0
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        monthly_revenue = Payment.objects.filter(status='completed', payment_date__gte=thirty_days_ago).aggregate(Sum('amount'))['amount__sum'] or 0.00 if Payment else 0.00
        upcoming_payments_sum = Payment.objects.filter(due_date__gte=today, due_date__lte=today + timedelta(days=30), status='pending').aggregate(Sum('amount'))['amount__sum'] or 0.00 if Payment else 0.00
        
        priority_tasks_data = [{'title': 'Oylik byudjet hisobotini tekshirish', 'url': '#', 'deadline': today + timedelta(days=5), 'color': 'text-red-500'}]

        context.update({
            'total_revenue': monthly_revenue,
            'active_teachers_count': total_teachers,
            'total_students_count': total_students,
            'active_groups': total_groups,
            'upcoming_payments_sum': upcoming_payments_sum,
            'recent_staff': recent_staff,
            'priority_tasks': priority_tasks_data,
            # date_joined CustomUser/AbstractUser maydoni. Bu yer to'g'ri.
            'new_teachers': CustomUser.objects.filter(role='teacher', date_joined__date=today).count(),
        })

        return render(request, "dashboard/boss_dashboard.html", context)

    # ---------------- TEACHER DASHBOARD ----------------
    
    # Faqat o'qituvchilar uchun mantiq
    if user.is_teacher:
        try:
            # CustomUser modeli Teacher modeliga 'teacher_profile' related_name orqali bog'langan deb faraz qilamiz
            teacher_profile = user.teacher_profile 
            
            # --- 1. Umumiy Statistikalar ---
            teacher_groups = Group.objects.filter(teacher=teacher_profile, is_active=True)
            total_groups = teacher_groups.count()
            total_students = Student.objects.filter(group__in=teacher_groups, is_active=True).count()
            
            teacher_tasks = Task.objects.filter(target_group__in=teacher_groups) if Task else Task.objects.none()
            
            # Tekshirilmagan Vazifalar Sonini hisoblash (is_completed=True, lekin feedback hali bo'sh)
            if TaskAssignment:
                pending_tasks_count = TaskAssignment.objects.filter(
                    task__in=teacher_tasks,
                    is_completed=True, # O'quvchi topshirgan
                    feedback="",       # Lekin o'qituvchi hali baho/izoh yozmagan
                ).count()
            else:
                pending_tasks_count = 0
            
            # --- 2. Kelgusi Darslar (Lesson modeli groups.models da mavjud) ---
            
            if Lesson:
                # Bugungi darslar soni
                today_lessons_count = Lesson.objects.filter(
                    group__in=teacher_groups, 
                    start_time__date=today
                ).count()

                # Kelgusi darslar (Hozirgi vaqtdan keyin keladigan 5 ta dars)
                upcoming_lessons_query = Lesson.objects.filter(
                    group__in=teacher_groups, 
                    start_time__gte=timezone.now()
                ).select_related('group').order_by('start_time')[:5] 

                upcoming_lessons = [
                    {'group_name': l.group.name, 
                     'time': l.start_time.strftime("%H:%M"), 
                     'date': l.start_time.date(), 
                     # get_lesson_type_display() Lesson modelida bo'lishi kerak
                     'type': l.get_lesson_type_display() 
                    }
                    for l in upcoming_lessons_query
                ]
            else:
                today_lessons_count = 0
                upcoming_lessons = []


            # --- 3. Tekshiruv Kutilayotgan Vazifalar Ro'yxati ---
            if Task and TaskAssignment:
                tasks_for_review_list = teacher_tasks.annotate(
                    pending_count=Count(
                        'assignments', 
                        filter=Q(
                            assignments__is_completed=True, # Topshirilgan
                            assignments__feedback=""        # Tekshirilmagan
                        )
                    )
                ).filter(pending_count__gt=0).order_by('-due_date')[:5] 
                
                tasks_for_review = [
                    {
                        'id': t.id, 
                        'title': t.title, 
                        'group_name': t.target_group.name if t.target_group else "-", 
                        'pending_count': t.pending_count # Annotate orqali hisoblangan son
                    }
                    for t in tasks_for_review_list
                ]
            else:
                tasks_for_review = []
                
            # --- 4. Contextga yuborish ---
            context.update({
                'teacher_profile': teacher_profile,
                'total_groups': total_groups,
                'total_students': total_students,
                'pending_tasks_count': pending_tasks_count,
                # Yangi qo'shilganlar
                'today_lessons_count': today_lessons_count,
                'upcoming_lessons': upcoming_lessons,
                'tasks_for_review': tasks_for_review,
            })
            
        except (AttributeError, Teacher.DoesNotExist):
            # Teacher profil bog'lanmagan bo'lsa
            messages.error(request, "Xato: Teacher profilingiz bog‘lanmagan.")
            context.update({
                'total_groups': 0, 'total_students': 0, 'pending_tasks_count': 0, 
                'today_lessons_count': 0, 'upcoming_lessons': [], 'tasks_for_review': []
            })
            
        return render(request, "dashboard/teacher_dashboard.html", context)

    # ---------------- STUDENT DASHBOARD ----------------
    if user.is_student:
        try:
            student_profile = user.student_profile
            group = student_profile.group
            group_name = group.name if group and group.is_active else "Guruhsiz"
            teacher_name = group.teacher.user.get_full_name() if group and group.teacher and group.teacher.user else "Tayinlanmagan"
            
            # O'quvchi o'ziga tayinlangan vazifalarni hisoblaydi
            if TaskAssignment:
                total_tasks = TaskAssignment.objects.filter(student=student_profile).count() 
                # Muddati o'tgan va bajarilmagan vazifalar
                overdue_tasks_count = TaskAssignment.objects.filter(
                    student=student_profile,
                    is_completed=False,
                    task__due_date__lt=timezone.now().date() # Faqat sanani tekshirish
                ).count()
            else:
                total_tasks = 0
                overdue_tasks_count = 0

            context.update({
                'student_profile': student_profile,
                'group_name': group_name,
                'teacher_name': teacher_name,
                'total_tasks': total_tasks,
                'overdue_tasks_count': overdue_tasks_count,
            })
        except (AttributeError, Student.DoesNotExist):
            messages.error(request, "Xato: Student profilingiz bog‘lanmagan.")
            context.update({'total_tasks': 0, 'overdue_tasks_count': 0})

        return render(request, "dashboard/student_dashboard.html", context)

    # Agar foydalanuvchi roli aniqlanmagan bo‘lsa
    return render(request, "dashboard/index.html", context)

# =========================
# PROFILE EDIT
# =========================
class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "phone", "avatar"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "border rounded w-full p-2"}),
            "last_name": forms.TextInput(attrs={"class": "border rounded w-full p-2"}),
            "email": forms.EmailInput(attrs={"class": "border rounded w-full p-2"}),
            "phone": forms.TextInput(attrs={"class": "border rounded w-full p-2"}),
            "avatar": forms.FileInput(attrs={"class": "border rounded w-full p-2"}),
        }

@login_required
def profile_edit_view(request):
    user = request.user
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil yangilandi ✅")
            return redirect("accounts:profile")
    else:
        form = ProfileForm(instance=user)
    return render(request, "accounts/profile_edit.html", {"form": form})