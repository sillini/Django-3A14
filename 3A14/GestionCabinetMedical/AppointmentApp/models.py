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

    appointment_date = models.DateTimeField()

    reason = models.TextField()

    prescription = models.FileField(
        upload_to='prescriptions/',
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf'])
        ]
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )

    duration_minutes = models.PositiveIntegerField(default=30)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()

        if self.appointment_date is None:
            return

        date_changed = self._state.adding

        if not self._state.adding:
            old_date = (
                type(self).objects
                .filter(pk=self.pk)
                .values_list('appointment_date', flat=True)
                .first()
            )
            date_changed = old_date != self.appointment_date

        if date_changed and self.appointment_date <= timezone.now():
            raise ValidationError({
                'appointment_date':
                    "La date du rendez-vous doit être dans le futur."
            })

    def __str__(self):
        return f"Rendez-vous: {self.patient} avec {self.doctor} le {self.appointment_date}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'appointment_date'],
                name='unique_doctor_appointment_date'
            )
        ]
        ordering = ['appointment_date']