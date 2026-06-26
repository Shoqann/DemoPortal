from django.test import TestCase
from django.urls import reverse
from .models import Employee, DepartureEvent
import datetime


class HiringNeedTests(TestCase):
    def setUp(self):
        e1 = Employee.objects.create(first_name='Ivan', last_name='Petrov')
        e2 = Employee.objects.create(first_name='Maria', last_name='Ivanova')
        DepartureEvent.objects.create(employee=e1, type=DepartureEvent.TYPE_RESIGNATION, date=datetime.date(2026, 1, 10))
        DepartureEvent.objects.create(employee=e2, type=DepartureEvent.TYPE_MATERNITY, date=datetime.date(2026, 2, 5))

    def test_api_counts(self):
        url = reverse('hiring_need_api')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn('by_type', data)
        types = {item['type']: item for item in data['by_type']}
        self.assertEqual(types['resignation']['count'], 1)
        self.assertEqual(types['maternity']['count'], 1)
