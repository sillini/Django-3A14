from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils import timezone


class Appointment(models.Model):

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'En attente'
        CONFIRMED = 'CONFIRMED', 'Confirmé'
        CANCELLED = 'CANCELLED', 'Annulé'

    doctor = models.ForeignKey(
        'AccountApp.Doctor',
        on_delete=models.CASCADE
    )

    patient = models.ForeignKey(
        'AccountApp.Patient',
        on_delete=models.CASCADE
    )

    appointment_date = models.DateTimeField(blank=False)

    reason = models.TextField(max_length=50, blank=True)

    prescription = models.FileField(
        upload_to='prescriptions/',
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf'],
            message="Seuls les fichiers PDF sont autorisés."
            )
        ]
    )

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'En attente'
        CONFIRMED = 'CONFIRMED', 'Confirmé'
        CANCELLED = 'CANCELLED', 'Annulé'

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )

    duration_minutes = models.PositiveIntegerField(default=30)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        date_changed = self._state.adding or(
            Appointment.objects.filter(
                    pk=self.pk,
                    appointment_date=self.appointment_date
            ).exists()
        )
        
        if date_changed and self.appointment_date <= timezone.now():
            raise ValidationError({
                'appointment_date':
                    "La date du rendez-vous doit être dans le futur."
            })

        
    def __str__(self):
        return f"Rendez-vous: {self.patient} avec {self.doctor} le {self.appointment_date}"

    class Meta():
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'appointment_date'],
                name='unique_doctor_appointment_date',
                violation_error_message="Le docteur a déjà un rendez-vous à cette date et heure."
            )
        ]
        ordering = ['appointment_date']