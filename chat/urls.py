from django.urls import path
from . import views

app_name = "chat"   # MUHIM, base.html da {% url 'chat:index' %} ishlashi uchun

urlpatterns = [
    path('', views.index, name='index'),   # /chat/
    path('<int:user_id>/', views.room, name='room'),
    path('<int:user_id>/messages/', views.get_messages, name='get_messages'),
    path('<int:user_id>/send/', views.send_message, name='send_message'),
]
