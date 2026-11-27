from django.contrib import admin
from .models import Doctor, Patient, Specialty

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Specialty)