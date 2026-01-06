from django import forms
from .models import Task
from groups.models import Group # Guruhlarni filtrlash uchun

class TaskForm(forms.ModelForm):
    # Vazifa turini radio tugmalar orqali tanlash uchun
    task_type = forms.ChoiceField(
        choices=Task.TASK_TYPE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'flex space-x-4'}),
        initial='Group',
        label="Vazifa turini tanlang"
    )

    class Meta:
        model = Task
        # created_by biz viewda avtomatik to'ldiramiz, shuning uchun formadan olib tashladik
        # assigned_teacher modeldan olib tashlanganligi sababli uni ham o'chiramiz
        fields = ['title', 'description', 'due_date', 'task_type', 'target_group', 'status'] 
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full border rounded-lg px-3 py-2 focus:ring-emerald-500'}),
            'description': forms.Textarea(attrs={'class': 'w-full border rounded-lg px-3 py-2 focus:ring-emerald-500', 'rows': 3}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full border rounded-lg px-3 py-2 focus:ring-emerald-500'}),
            # target_group endi guruh maydoni
            'target_group': forms.Select(attrs={'class': 'w-full border rounded-lg px-3 py-2 focus:ring-emerald-500'}),
            'status': forms.Select(attrs={'class': 'w-full border rounded-lg px-3 py-2 focus:ring-emerald-500'}),
        }
        labels = {
            'target_group': 'Maqsadli guruh',
            'due_date': 'Topshirish sanasi',
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        # JORIY O'QITUVCHIGA TEGISHLI GURUH FILTRINI QO'SHISH
        if user and user.is_authenticated:
            if hasattr(user, 'is_teacher') and user.is_teacher:
                # O'qituvchiga faqat o'zi dars beradigan guruhlarni ko'rsatish
                self.fields['target_group'].queryset = Group.objects.filter(teacher__user=user)
            elif user.is_superuser or user.is_boss:
                # Admin barcha guruhlarni ko'ra oladi
                self.fields['target_group'].queryset = Group.objects.all()
            else:
                # Boshqa foydalanuvchilarga guruh tanlashga ruxsat yo'q
                 self.fields['target_group'].queryset = Group.objects.none()
                 
        # target_student ni keyinchalik qo'shganingizda, uni shu yerda boshqarasiz.
        # Masalan: self.fields['target_student'].required = False