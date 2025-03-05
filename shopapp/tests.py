from django.test import TestCase
from .models import *
from django.contrib.auth.models import User
from .forms import OrderForm
from urllib.parse import urlencode


data = urlencode({
    'title': 'My Title',
    'content': 'this is a my title content'
})

invalid_data = urlencode({
    'title': '',
    'content': 'this is a new content'
})

"""
Testing views
working with models
authenticated views
setting headers

Testing forms
testing validation
test custom validation
test integration with views

Testing APIs
"""

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
        print(res, res.status_code)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(Order.objects.count(), 1)


class TestViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.post = Post.objects.create(title='test post', content='this is a test post')
        cls.user = User.objects.create_user(username='admin', password='pass123')
    
    def test_set_up(self):
        print('Testing set up!')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().username, 'admin')

    def test_unauth_get_posts_view(self):
        res = self.client.get('/getposts/')
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, '/signin/?next=/getposts/')
    
    def test_auth_get_posts_view(self):
        logged_in = self.client.login(username=self.user.username, password='pass123')
        print(logged_in)
        res = self.client.get('/getposts/', headers={'X-Coder': 'Chidera Valentine'})
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'posts')
    
    def test_valid_create_post_view(self):
        res = self.client.post(path='/createpost/', data=data, content_type='application/x-www-form-urlencoded')
        print(res, res.status_code)
        self.assertEqual(res.status_code, 302)
        logged_in = self.client.login(username=self.user.username, password='pass123')
        print(logged_in)
        self.assertRedirects(res, '/getposts/')
        self.assertEqual(Post.objects.count(), 2)
    
    def test_invalid_create_post_view(self):
        res = self.client.post(path='/createpost/', data=invalid_data, content_type='application/x-www-form-urlencoded')
        print(res.content)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(Post.objects.count(), 1)
    
    def test_valid_edit_post_view(self):
        res = self.client.post(path='/editpost/1/', data=data, content_type='application/x-www-form-urlencoded')
        print(res.content)
        self.assertEqual(res.status_code, 302)
        logged_in = self.client.login(username=self.user.username, password='pass123')
        print(logged_in)
        self.assertRedirects(res, '/getposts/')
    
    def test_invalid_edit_post_view(self):
        res = self.client.post(path='/editpost/100/', data=data, content_type='application/x-www-form-urlencoded')
        print(res.content)
        self.assertEqual(res.status_code, 200)
        self.assertIn(res.content.decode(), ['Post does not exist', 'Invalid edit post data'])
    
    def test_valid_delete_post_view(self):
        res = self.client.post(path='/deletepost/1/')
        print(res.content)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(Post.objects.count(), 0)
    
    def test_invalid_delete_post_view(self):
        res = self.client.post(path='/deletepost/100/')
        print(res.content)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(Post.objects.count(), 1)
            
