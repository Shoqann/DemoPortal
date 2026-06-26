from django.contrib import admin
from .models import Employee, DepartureEvent


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'position', 'is_active')


@admin.register(DepartureEvent)
class DepartureEventAdmin(admin.ModelAdmin):
    list_display = ('employee', 'type', 'date')
    list_filter = ('type', 'date')
