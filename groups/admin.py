from django.contrib import admin
from .models import Group
# Students modeliga kirish uchun Count dan foydalanish uchun import qilinadi
from django.db.models import Count, Q 

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    # MUHIM O'ZGARTIRISH: "students_count" o'rniga yangi usul nomi qo'yildi
    list_display = ("name", "teacher", "get_active_students_count_admin", "created_at")
    
    # Qidiruv maydonlari
    search_fields = ("name", "teacher__user__first_name", "teacher__user__last_name") 
    
    list_filter = ("teacher", "is_active", "type", "created_at") # Modelga type qo'shilganligi uchun

    # -------------------------------------------------------------
    # YANGI USUL: Admin Panelda Faol Talabalar Sonini Ko'rsatish
    # -------------------------------------------------------------
    def get_active_students_count_admin(self, obj):
        # Model obyektiga 'students' orqali ulanib, faol talabalar sonini hisoblaymiz
        return obj.students.filter(is_active=True).count()
        
    get_active_students_count_admin.short_description = "Faol o‘quvchilar soni"
    
    # =============================================================
    # ROLGA ASOSLANGAN RUHSATLAR (O'zgartirishsiz qoldi)
    # =============================================================

    def has_add_permission(self, request):
        # Guruh qo'shish ruxsati faqat Boss yoki Superuserga beriladi
        # is_boss maydoni CustomUser modelida mavjud deb taxmin qilamiz
        return request.user.is_boss or request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        # Guruhni o'zgartirish ruxsati faqat Boss yoki Superuserga beriladi
        return request.user.is_boss or request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        # Guruhni o'chirish ruxsati faqat Boss yoki Superuserga beriladi
        return request.user.is_boss or request.user.is_superuser
        
    def has_view_permission(self, request, obj=None):
        # Ko'rish ruxsati barcha avtorizatsiyadan o'tgan foydalanuvchilarga beriladi
        return True