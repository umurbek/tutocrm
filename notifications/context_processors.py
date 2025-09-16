from .models import Notification
from teachers.models import Teacher

def unread_notifications(request):
    if request.user.is_authenticated:
        try:
            teacher = Teacher.objects.get(email=request.user.email)
            unread_qs = Notification.objects.filter(teacher=teacher, is_read=False).order_by("-created_at")
            return {
                "unread_count": unread_qs.count(),
                "unread_list": unread_qs[:5],
            }
        except Teacher.DoesNotExist:
            return {"unread_count": 0, "unread_list": []}
    return {"unread_count": 0, "unread_list": []}
