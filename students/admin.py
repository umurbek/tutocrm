# students/admin.py

from django.contrib import admin
from .models import Student
from .forms import StudentCreateForm # Yangi talaba yaratish formasi uchun
from django.utils.html import format_html

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # Ro'yxat ko'rinishi
    list_display = (
        'id', 
        'student_full_name',  # Custom metod: foydalanuvchining to'liq ismini chiqarish
        'student_email',      # Custom metod: foydalanuvchining emailini chiqarish
        'group',              # Student modelidagi ForeignKey
        'payment',            # Student modelidagi DecimalField
        'join_date',          # Student modelidagi sana
        'is_active',          # Student modelidagi Boolean
    )
    
    # Ro'yxat bo'yicha filtrlash
    list_filter = ('group', 'is_active', 'join_date')
    
    # Qidiruv (CustomUser orqali ism va emailni qidirish uchun)
    search_fields = (
        'user__first_name', 
        'user__last_name', 
        'user__email', 
        'group__name'
    )
    
    # Detail sahifasida maydonlarni tartiblash va guruhlash
    fieldsets = (
        ("Foydalanuvchi ma'lumotlari (CustomUser)", {
            'fields': ('user',),
            'description': "Avval yaratilgan foydalanuvchini tanlang."
        }),
        ("Talabalik Ma'lumotlari", {
            'fields': ('group', 'payment', 'is_active'),
        }),
    )

    # ==========================================================
    # Custom metodlar (list_display da foydalaniladi)
    # ==========================================================
    
    # 1. Talabaning to'liq ismini chiqarish
    @admin.display(description='F.I.SH')
    def student_full_name(self, obj):
        return obj.user.get_full_name() if obj.user else "---"
        
    # 2. Talabaning email manzilini chiqarish
    @admin.display(description='Email')
    def student_email(self, obj):
        return obj.user.email if obj.user else "---"

    # ==========================================================
    # Yangi Student yaratishni alohida form orqali boshqarish (ixtiyoriy)
    # ==========================================================

    # Yangi obyekt yaratish uchun forma (Agar siz StudentCreateForm dan foydalanmoqchi bo'lsangiz)
    # add_form = StudentCreateForm 
    
    # def get_form(self, request, obj=None, **kwargs):
    #     if not obj: # Agar yangi obyekt yaratish sahifasi bo'lsa
    #         return self.add_form
    #     return super().get_form(request, obj, **kwargs)

    # Yuqoridagi kommentariyadagi qismlar, agar siz alohida yaratish formasini ishlatmoqchi bo'lsangiz kerak bo'ladi.