from django.core.validators import MinLengthValidator, RegexValidator,MaxLengthValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Doctor(User):
    license_number = models.CharField(
        max_length=6,
        unique=True,
        blank=False,
        validators=[MinLengthValidator(6),MaxLengthValidator(6)]
    )

    phone = models.CharField(max_length=8,unique=True)

    specialties = models.ManyToManyField('Specialty')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta():
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"
    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}"

def validate_past_date(value):
    if value >= timezone.localdate():
        raise ValidationError(
            "La date de naissance doit être antérieure à aujourd'hui."
        )
class Patient(User):
    national_id = models.CharField(
        max_length=8,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{8}$',
                message="Le CIN doit contenir exactement 8 chiffres."
            )
        ]
    )

    phone = models.CharField(
        max_length=8,
        validators=[
            RegexValidator(
                regex=r'^\d{8}$',
                message="Le téléphone doit contenir exactement 8 chiffres."
            )
        ]
    )

    birth_date = models.DateField(
        validators=[validate_past_date]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Specialty(models.Model):
    name = models.CharField(max_length=50,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name