from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Employee(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    position = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)

    @property
    def age(self):
        if not self.birth_date:
            return None
        today = timezone.now().date()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class DepartureEvent(models.Model):
    TYPE_RESIGNATION = 'resignation'
    TYPE_MATERNITY = 'maternity'
    TYPE_RETIREMENT = 'retirement'
    TYPE_DISMISSAL_VIOLATION = 'dismissal_violation'
    TYPE_DISMISSAL_CERT = 'dismissal_cert'
    TYPE_OTHER = 'other'

    TYPE_CHOICES = [
        (TYPE_RESIGNATION, 'По собственному желанию'),
        (TYPE_MATERNITY, 'Декрет / отпуск по уходу'),
        (TYPE_RETIREMENT, 'Выход на пенсию'),
        (TYPE_DISMISSAL_VIOLATION, 'Увольнение за нарушения'),
        (TYPE_DISMISSAL_CERT, 'Увольнение по аттестации'),
        (TYPE_OTHER, 'Другое'),
    ]

    employee = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.SET_NULL)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    date = models.DateField()
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_type_display()} — {self.date}"
