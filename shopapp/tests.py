from django.test import TestCase
from .models import *
from django.contrib.auth.models import User
from .forms import OrderForm
from urllib.parse import urlencode


class TestForm(TestCase):
    def test_valid_form(self):
        form = OrderForm(data={
            'first_name': 'Kevin',
            'last_name': 'Hart',
            'email': 'hart@gmail.com',
            'phone': '09184522718',
            'address': 'United states',
            'state': 'Los Angeles',
            'zip_code': 1234567
        })
        self.assertTrue(form.is_valid())
    
    def test_invalid_form(self):
        form = OrderForm(data={
            'first_name': 'Kevin',
            'last_name': 'Hart',
            'email': 'hart@gmail.com',
            'phone': '0918452202318',
            'address': 'United states',
            'state': 'Los Angeles',
        })
        self.assertFalse(form.is_valid())

    def test_form_in_view(self):
        data=urlencode({
            'first_name': 'Kevin',
            'last_name': 'Hart',
            'email': 'hart@gmail.com',
            'phone': '0918452218',
            'address': 'United states',
            'state': 'Los Angeles',
            'zip_code': 3839383
        })
        
        res = self.client.post(path='/cart/', data=data, content_type='application/x-www-form-urlencoded')
        self.assertEqual(res.status_code, 302)
        self.assertEqual(Order.objects.count(), 1)


