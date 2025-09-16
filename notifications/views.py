from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification
from teachers.models import Teacher


@login_required
def notification_list(request):
    try:
        teacher = Teacher.objects.get(email=request.user.email)
        notifications = Notification.objects.filter(teacher=teacher).order_by("-created_at")
    except Teacher.DoesNotExist:
        notifications = []  # oddiy user bo‘lsa, hech narsa chiqmaydi

    return render(request, "notifications/list.html", {"notifications": notifications})


@login_required
def mark_as_read(request, pk):
    try:
        teacher = Teacher.objects.get(email=request.user.email)
        notif = get_object_or_404(Notification, pk=pk, teacher=teacher)
    except Teacher.DoesNotExist:
        return redirect("notification_list")

    notif.is_read = True
    notif.save()
    if notif.url:
        return redirect(notif.url)
    return redirect("notification_list")
