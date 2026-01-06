from datetime import timedelta
from decimal import Decimal

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.db.models import Sum, Avg, Count, Q, DecimalField
from django.db.models.functions import Coalesce, TruncMonth

# ===========================
# MODELLAR
# ===========================
from .models import DashboardStat, MonthlyExpense
from .forms import DashboardStatsForm, MonthlyExpenseForm

from accounts.models import CustomUser
from students.models import Student
from groups.models import Group

try:
    from payments.models import Payment
except ImportError:
    Payment = None

try:
    from teachers.models import Teacher
except ImportError:
    Teacher = None

try:
    from tasks.models import Task, Submission
except ImportError:
    Task = Submission = None

try:
    from groups.models import Lesson
except ImportError:
    Lesson = None


# ===========================
# ASOSIY DASHBOARD VIEW
# ===========================
@login_required
def dashboard_view(request):
    user = request.user
    now = timezone.now()
    today = now.date()

    if getattr(user, 'is_student', False):
        return student_dashboard(request, user, now, today)

    if getattr(user, 'is_boss', False):
        return boss_dashboard(request, user, now, today)

    if getattr(user, 'is_teacher', False):
        return teacher_dashboard(request, user, now)

    messages.warning(request, "Siz uchun maxsus dashboard mavjud emas.")
    return render(request, "dashboard/default_dashboard.html", {"user_role": user.role})


# ===========================
# STUDENT DASHBOARD
# ===========================
def student_dashboard(request, user, now, today):
    try:
        student = Student.objects.select_related("group", "user").get(user=user, is_active=True)
        group = student.group
    except Student.DoesNotExist:
        messages.error(request, "Talaba profilingiz topilmadi.")
        return render(request, "dashboard/student_dashboard.html")

    # --- TO‘LOV HOLATI ---
    payment_status = "To‘langan"
    next_payment_date = None

    if Payment:
        payment = Payment.objects.filter(
            student=student,
            status__in=["Pending", "Overdue"]
        ).order_by("due_date").first()

        if payment:
            next_payment_date = payment.due_date
            payment_status = "Overdue" if payment.due_date < today else "Pending"

    # --- O‘RTACHA BAHO ---
    average_grade = "N/A"
    if Submission:
        avg = Submission.objects.filter(
            student=student,
            score__isnull=False
        ).aggregate(avg=Avg("score"))["avg"]

        if avg is not None:
            average_grade = f"{avg:.1f}%"

    # --- MUDDATI O‘TGAN TOPSHIRIQLAR ---
    overdue_tasks_count = 0
    submitted_ids = []

    if Task and Submission and group:
        submitted_ids = Submission.objects.filter(
            student=student,
            status="completed"
        ).values_list("task_id", flat=True)

        overdue_tasks_count = Task.objects.filter(
            group=group,
            deadline__lt=now
        ).exclude(id__in=submitted_ids).count()

    # --- KELGUSI DARSLAR ---
    upcoming_lessons = []
    if Lesson and group:
        lessons = Lesson.objects.filter(
            group=group,
            start_time__gte=now
        ).select_related("group__teacher__user").order_by("start_time")[:5]

        for lesson in lessons:
            upcoming_lessons.append({
                "group": lesson.group.name,
                "teacher": lesson.group.teacher.user.get_full_name() if lesson.group.teacher else "N/A",
                "date": lesson.start_time.date(),
                "time": lesson.start_time.time(),
            })

    # --- YAQIN TOPSHIRIQLAR ---
    urgent_tasks = []
    if Task and group:
        urgent_tasks = Task.objects.filter(
            group=group,
            deadline__range=(now, now + timedelta(days=7))
        ).exclude(id__in=submitted_ids).order_by("deadline")[:5]

    context = {
        "student": student,
        "payment_status": payment_status,
        "next_payment_date": next_payment_date,
        "average_grade": average_grade,
        "overdue_tasks_count": overdue_tasks_count,
        "upcoming_lessons": upcoming_lessons,
        "urgent_tasks": urgent_tasks,
        "user_role": user.role,
    }

    return render(request, "dashboard/student_dashboard.html", context)


# ===========================
# BOSS (ADMIN) DASHBOARD
# ===========================
def boss_dashboard(request, user, now, today):
    thirty_days_ago = now - timedelta(days=30)
    thirty_days_later = now + timedelta(days=30)

    active_groups = Group.objects.filter(is_active=True).count()
    total_students = Student.objects.filter(is_active=True).count()

    active_teachers = Teacher.objects.filter(is_active=True).count() if Teacher else 0
    new_teachers = Teacher.objects.filter(
        is_active=True,
        user__date_joined__gte=thirty_days_ago
    ).count() if Teacher else 0

    total_revenue = Decimal("0.00")
    upcoming_payments = Decimal("0.00")
    labels, values = [], []

    if Payment:
        success_status = ["paid", "completed"]

        total_revenue = Payment.objects.filter(
            status__in=success_status
        ).aggregate(
            total=Coalesce(Sum("amount"), Decimal("0.00"), output_field=DecimalField())
        )["total"]

        upcoming_payments = Payment.objects.filter(
            status="Pending",
            due_date__range=(today, thirty_days_later)
        ).aggregate(
            total=Coalesce(Sum("amount"), Decimal("0.00"), output_field=DecimalField())
        )["total"]

        chart_data = Payment.objects.filter(
            status__in=success_status,
            created_at__gte=now - timedelta(days=365)
        ).annotate(
            month=TruncMonth("created_at")
        ).values("month").annotate(
            total=Sum("amount")
        ).order_by("month")

        labels = [d["month"].strftime("%b %Y") for d in chart_data]
        values = [float(d["total"]) for d in chart_data]

    priority_tasks = []
    if Payment:
        overdue_count = Payment.objects.filter(status="Overdue").count()
        try:
            url = reverse("payments:overdue_list")
        except NoReverseMatch:
            url = "#"

        priority_tasks.append({
            "title": f"{overdue_count} ta qarzdor student",
            "url": url,
            "color": "text-red-600",
            "deadline": today,
        })

    recent_staff = CustomUser.objects.filter(
        role__in=["boss", "teacher"]
    ).order_by("-date_joined")[:10]

    context = {
        "active_groups": active_groups,
        "total_students": total_students,
        "active_teachers": active_teachers,
        "new_teachers": new_teachers,
        "total_revenue": total_revenue,
        "upcoming_payments": upcoming_payments,
        "priority_tasks": priority_tasks,
        "recent_staff": recent_staff,
        "monthly_revenue_labels": labels,
        "monthly_revenue_values": values,
        "user_role": user.role,
    }

    return render(request, "dashboard/boss_dashboard.html", context)


# ===========================
# TEACHER DASHBOARD
# ===========================
def teacher_dashboard(request, user, now):
    try:
        teacher = Teacher.objects.get(user=user, is_active=True)
    except Teacher.DoesNotExist:
        messages.error(request, "O‘qituvchi profilingiz topilmadi.")
        return render(request, "dashboard/teacher_dashboard.html")

    groups_count = Group.objects.filter(teacher=teacher, is_active=True).count()
    students_count = Student.objects.filter(group__teacher=teacher, is_active=True).count()

    lessons = []
    today_lessons = 0

    if Lesson:
        lessons = Lesson.objects.filter(
            group__teacher=teacher,
            start_time__gte=now
        ).order_by("start_time")[:5]

        today_lessons = Lesson.objects.filter(
            group__teacher=teacher,
            start_time__date=now.date()
        ).count()

    context = {
        "teacher": teacher,
        "total_groups": groups_count,
        "total_students": students_count,
        "upcoming_lessons": lessons,
        "today_lessons_count": today_lessons,
        "user_role": user.role,
    }

    return render(request, "dashboard/teacher_dashboard.html", context)


# ===========================
# STAT INPUT
# ===========================
@login_required
def stats_input_view(request):
    form = DashboardStatsForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        stat = form.save(commit=False)
        stat.user = request.user
        stat.save()
        return redirect("dashboard:dashboard_view")
    return render(request, "dashboard/input.html", {"form": form})


# ===========================
# EXPENSE INPUT
# ===========================
@login_required
def expense_input_view(request):
    form = MonthlyExpenseForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        expense = form.save(commit=False)
        expense.user = request.user
        expense.save()
        messages.success(request, "Xarajat qo‘shildi.")
        return redirect("dashboard:dashboard_view")
    return render(request, "dashboard/expense_input.html", {"form": form})


# ===========================
# EXPENSE CHART APIs
# ===========================
@login_required
def expense_chart_view(request):
    qs = MonthlyExpense.objects.all() if request.user.is_boss else MonthlyExpense.objects.filter(user=request.user)
    data = qs.values("month").annotate(total=Sum("amount")).order_by("month")
    return JsonResponse({
        "labels": [d["month"] for d in data],
        "data": [float(d["total"]) for d in data],
    })


@login_required
def expense_pie_chart_view(request):
    qs = MonthlyExpense.objects.all() if request.user.is_boss else MonthlyExpense.objects.filter(user=request.user)
    return JsonResponse(list(qs.values("category").annotate(total=Sum("amount"))), safe=False)


@login_required
def recent_expense_chart_view(request):
    since = timezone.now() - timedelta(days=30)
    qs = MonthlyExpense.objects.filter(created_at__gte=since)
    if not request.user.is_boss:
        qs = qs.filter(user=request.user)

    data = [{"month": e.month, "amount": float(e.amount), "category": e.category} for e in qs]
    return JsonResponse(data, safe=False)
