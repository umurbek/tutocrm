from django.urls import path
from . import views

app_name = "groups"

urlpatterns = [
    path('', views.group_list, name='group_list'),
    path('new/', views.group_create, name='group_create'),
    path('<int:pk>/', views.group_detail, name='group_detail'),   # ✅ qo‘shildi
    path('<int:pk>/edit/', views.group_update, name='group_update'),
    path('<int:pk>/delete/', views.group_delete, name='group_delete'),
    path('schedule/', views.schedule_view, name='schedule'),
    path('lesson/<int:pk>/attendance/', views.lesson_attendance, name='attendance'),
]
