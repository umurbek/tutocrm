from django.db import models

class SystemSettings(models.Model):
    crm_name = models.CharField(max_length=100, default="TutorCRM")
    language = models.CharField(max_length=20, choices=[("uz", "O‘zbekcha"), ("en", "English")], default="uz")
    currency = models.CharField(max_length=10, default="UZS")
    logo = models.ImageField(upload_to="logos/", blank=True, null=True)

    def __str__(self):
        return self.crm_name
