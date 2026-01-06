from .models import Notification
from teachers.models import Teacher
# CustomUser va boshqa rollarni qo'shish uchun CustomUser modelini ham import qilish yaxshi amaliyot:
# from accounts.models import CustomUser 
# Agar Notification modeli faqat Teacher/Studentga emas, balki CustomUserga bog'langan bo'lsa, pastdagi kodni almashtirish kerak.

def unread_notifications(request):
    if request.user.is_authenticated:
        
        # 💡 MUAMMONING YECHIMI: 
        # Teacher modelida 'email' maydoni yo'q. U CustomUser bilan 'user' orqali bog'langan.
        # Teacher profilini CustomUser orqali topamiz (related_name='teacher_profile' deb faraz qilinadi)

        # 1. Agar foydalanuvchi o'qituvchi ekanligiga amin bo'lsak:
        if request.user.is_teacher:
            try:
                # Eng to'g'ri usul: OneToOneField orqali bog'langan profilni chaqirish
                teacher = request.user.teacher_profile
                
                # Agar Notification modeli teacher (Teacher modeli)ga bog'langan bo'lsa:
                unread_qs = Notification.objects.filter(teacher=teacher, is_read=False).order_by("-created_at")
                
                return {
                    "unread_count": unread_qs.count(),
                    "unread_list": unread_qs[:5],
                }
            except Teacher.DoesNotExist:
                 # Agar CustomUser bor, lekin Teacher profili bog'lanmagan bo'lsa
                return {"unread_count": 0, "unread_list": []}
            except AttributeError:
                # Agar user.is_teacher true, lekin teacher_profile yo'q bo'lsa (yoki related_name boshqacha bo'lsa)
                # Bu yerda xato xabarni loglashingiz mumkin.
                return {"unread_count": 0, "unread_list": []}

        # 2. Boshqa rollar (Student, Boss, Admin) uchun hisoblashni qo'shish
        
        # Agar Notification to'g'ridan-to'g'ri CustomUser (recipient)ga bog'langan bo'lsa:
        # if not request.user.is_teacher:
        #     unread_qs = Notification.objects.filter(recipient=request.user, is_read=False).order_by("-created_at")
        #     return {
        #         "unread_count": unread_qs.count(),
        #         "unread_list": unread_qs[:5],
        #     }


    # Agar foydalanuvchi login qilmagan bo'lsa
    return {"unread_count": 0, "unread_list": []}