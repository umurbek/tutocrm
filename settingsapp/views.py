from django.shortcuts import render, redirect
from .models import SystemSettings
from .forms import SystemSettingsForm

def settings_view(request):
    settings_obj, created = SystemSettings.objects.get_or_create(id=1)

    if request.method == "POST":
        form = SystemSettingsForm(request.POST, request.FILES, instance=settings_obj)
        if form.is_valid():
            form.save()
            return redirect('settings')
    else:
        form = SystemSettingsForm(instance=settings_obj)

    return render(request, "settingsapp/settings.html", {"form": form})
