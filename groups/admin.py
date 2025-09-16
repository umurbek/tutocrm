from django.contrib import admin
from .models import Group

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "teacher", "students_count", "created_at")
    search_fields = ("name", "teacher")
    list_filter = ("teacher", "created_at")
