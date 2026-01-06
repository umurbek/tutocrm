from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    # bosh sahifa login sahifaga yuboradi
    path('', lambda request: redirect('accounts:email_login'), name='home'),

    path('auth/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('accounts/', include('allauth.urls')),
    path('dashboard/', include(('dashboard.urls', 'dashboard'), namespace='dashboard')),
    path('groups/', include(('groups.urls', 'groups'), namespace='groups')),
    path('students/', include(('students.urls', 'students'), namespace='students')),
    path('teachers/', include(('teachers.urls', 'teachers'), namespace='teachers')),
    path('tasks/', include(('tasks.urls', 'tasks'), namespace='tasks')),
    path('settings/', include(('settingsapp.urls', 'settingsapp'), namespace='settingsapp')),
    path('notifications/', include(('notifications.urls', 'notifications'), namespace='notifications')),
    path('chat/', include(('chat.urls', 'chat'), namespace='chat')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
