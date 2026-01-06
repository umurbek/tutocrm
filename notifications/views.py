from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification
from teachers.models import Teacher
from students.models import Student # Agar kelajakda kerak bo'lsa, uni ham import qiling


@login_required
def notification_list(request):
    user = request.user
    notifications = Notification.objects.none()

    # 💡 MUAMMONING YECHIMI: user__email o'rniga, bog'langan profildan foydalanish
    if user.is_teacher: # Agar CustomUser modelida is_teacher maydoni bo'lsa
        try:
            # Eng samarali usul: OneToOneField orqali bog'langan profilni chaqirish
            teacher = user.teacher_profile 
            
            # Agar Notification modelida 'teacher' ForeignKey maydoni bo'lsa
            notifications = Notification.objects.filter(teacher=teacher).order_by("-created_at")
            
            # Faqat Teacher uchun ko'rilmaganlarni ko'rildi deb belgilash (ixtiyoriy)
            Notification.objects.filter(teacher=teacher, is_read=False).update(is_read=True)

        except (AttributeError, Teacher.DoesNotExist):
            # Teacher profili topilmasa (yoki bog'lanmagan bo'lsa)
            pass

    # Agar boshqa rollar uchun ham bildirishnomalar kerak bo'lsa, shu yerda qo'shing
    # elif user.is_student:
    #     try:
    #         student = user.student_profile
    #         notifications = Notification.objects.filter(student=student).order_by("-created_at")
    #         Notification.objects.filter(student=student, is_read=False).update(is_read=True)
    #     except (AttributeError, Student.DoesNotExist):
    #         pass
            
    return render(request, "notifications/list.html", {"notifications": notifications})


@login_required
def mark_as_read(request, pk):
    user = request.user
    
    # 💡 MUAMMONING YECHIMI: user__email o'rniga, bog'langan profildan foydalanish
    if user.is_teacher:
        try:
            # Teacher obyektini olish
            teacher = user.teacher_profile 
            
            # Bildirishnomani pk va shu o'qituvchiga tegishli ekanligini tekshirib olish
            notif = get_object_or_404(Notification, pk=pk, teacher=teacher)
            
        except (AttributeError, Teacher.DoesNotExist):
            # Agar profil topilmasa yoki CustomUserda teacher_profile mavjud bo'lmasa
            return redirect("notification_list")
            
        except Notification.DoesNotExist:
             # Agar bildirishnoma mavjud bo'lmasa yoki boshqa o'qituvchiga tegishli bo'lsa
             return redirect("notification_list")
    
    # Boshqa rollar (Student, Boss) uchun ham qoidalar qo'shish kerak.
    # Agar Notification modeli to'g'ridan-to'g'ri CustomUserga bog'langan bo'lsa, qidiruvni soddalashtirish mumkin.
    
    else: # Agar foydalanuvchi Teacher bo'lmasa, uni to'g'ri qidiruv sahifasiga yo'naltiramiz
        return redirect("notification_list")


    # Muvaffaqiyatli topilsa
    notif.is_read = True
    notif.save()
    
    # URLga yo'naltirish
    if notif.url:
        return redirect(notif.url)
        
    return redirect("notification_list")