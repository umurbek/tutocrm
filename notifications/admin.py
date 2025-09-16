from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "teacher", "is_read", "created_at")  # user → teacher
    list_filter = ("is_read", "created_at")
    search_fields = ("title", "message", "teacher__name")  # user__username emas
