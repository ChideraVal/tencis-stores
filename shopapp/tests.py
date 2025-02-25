from django.test import TestCase
from .models import *
import json

data = json.dumps({
    'title': 'new title',
    'content': 'this is a new content'
})

invalid_data = json.dumps({
    'title': '',
    'content': 'this is a new content'
})

# Test views, models, forms

"""
Testing views
working with models
authenticated views
"""


class TestViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.post = Post.objects.create(title='test post', content='this is a test post')
    
    def test_get_posts_view(self):
        res = self.client.get('/getposts/')
        print(res.content)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'posts')
    
    def test_valid_create_post_view(self):
        res = self.client.post(path='/createpost/', data=data, content_type='application/json')
        print(res.content)
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, '/getposts/')
        self.assertEqual(Post.objects.count(), 2)
    
    def test_invalid_create_post_view(self):
        res = self.client.post(path='/createpost/', data=invalid_data, content_type='application/json')
        print(res.content)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(Post.objects.count(), 1)
    
    def test_valid_edit_post_view(self):
        res = self.client.post(path='/editpost/1/', data=data, content_type='application/json')
        print(res.content)
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, '/getposts/')
    
    def test_invalid_edit_post_view(self):
        res = self.client.post(path='/editpost/100/', data=data, content_type='application/json')
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
            

