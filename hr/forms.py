from django import forms
from .models import Employee, DepartureEvent


class EmployeeRegistrationForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'birth_date', 'position']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }


class DepartureEventForm(forms.ModelForm):
    class Meta:
        model = DepartureEvent
        fields = ['employee', 'date', 'note']
        labels = {
            'employee': 'Сотрудник',
            'date': 'Дата события',
            'note': 'Комментарий',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'note': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Причина, номер приказа или важная заметка'}),
        }
