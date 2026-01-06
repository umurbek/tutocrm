from django.contrib import admin
from .models import Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'teacher_full_name',  # 👈 name o‘rniga
        'subject',
        'is_active',
    )

    search_fields = (
        'user__first_name',
        'user__last_name',
        'user__email',
        'subject',
    )

    list_filter = ('is_active', 'subject')

    # =====================
    # Custom display method
    # =====================
    @admin.display(description="F.I.Sh")
    def teacher_full_name(self, obj):
        return obj.user.get_full_name() if obj.user else "-"
