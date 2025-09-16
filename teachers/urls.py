from django.urls import path
from . import views

app_name = "teachers"

urlpatterns = [
    path('', views.teacher_list, name='teacher_list'),
    path('new/', views.teacher_create, name='teacher_create'),
    path('<int:pk>/edit/', views.teacher_update, name='teacher_update'),
    path('<int:pk>/delete/', views.teacher_delete, name='teacher_delete'),
]
