# students/forms.py

from django import forms
from .models import Student
from accounts.models import CustomUser 
from groups.models import Group

# 1. 🎓 Mavjud Student profilini tahrirlash formasi (Admin/Update uchun)
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        # Endi bu maydonlar models.py dagi maydonlarga mos keladi va xato bermaydi!
        fields = ['user', 'group', 'payment', 'is_active']
        
        # Sizning custom widgetlaringiz
        widgets = {
            'user': forms.Select(attrs={
                 'class': 'w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500'
            }), 
            'group': forms.Select(attrs={
                 'class': 'w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500'
            }),
            'payment': forms.NumberInput(attrs={
                 'class': 'w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500'
            }),
            'is_active': forms.CheckboxInput(attrs={
                 'class': 'form-checkbox h-5 w-5 text-indigo-600'
            }),
        }

# 2. ➕ Yangi Student va CustomUser'ni bir vaqtda yaratish formasi (Create uchun)
# Bu forma Admin panelda emas, balki loyiha interfeysida foydali bo'ladi.
class StudentCreateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Student
        fields = ['group', 'payment']

    def save(self, commit=True):
        user = CustomUser.objects.create_user(
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            phone=self.cleaned_data['phone'],
            role='student',
        )

        student = super().save(commit=False)
        student.user = user
        if commit:
            student.save()
        return student

# 2. ➕ Yangi Student va CustomUser'ni bir vaqtda yaratish formasi (Yangi ehtiyoj uchun)
# Bu forma hozirgi xatoingizni hal qilmaydi, lekin loyiha mantiqi uchun juda muhim!
