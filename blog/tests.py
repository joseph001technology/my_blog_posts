from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.test import TestCase

from blog.constants import PUBLISHED
from blog.models import Post


# Create your tests here.

User = get_user_model()

class TestUrls(TestCase):
    def test_add_url(self):
        url = reverse('blog:add')
        self.assertEqual(url, '/blog/add/')
        
    def test_posts_url(self):
        url = reverse('blog:personal_home')
        self.assertEqual(url, '/blog/home/')
        
        
    def test_search_url(self):
        url = reverse('blog:post_search')
        self.assertEqual(url, '/blog/search/')
        
    def test_single_post_url(self):
        url = reverse('blog:post_single', args=['sample-slug'])
        self.assertEqual(url, '/blog/sample-slug/')
        
    def test_edit_url(self):
            url = reverse('blog:edit', args=[1])
            self.assertEqual(url, '/blog/edit/1/')
         
    def test_delete_url(self):
            url = reverse('blog:delete', args=[1])
            self.assertEqual(url, '/blog/delete/1/')
            
            


class TestViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.post = Post.newmanager.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            content='This is a test post body.',
            status=PUBLISHED
            
        )
        self.post.favourites.add(self.user)  # Add user to favourites

    def test_home_view(self):
        response = self.client.get(reverse('blog:homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogtemplates/index.html')

    def test_personal_home_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('blog:personal_home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogtemplates/home.html')

    def test_personal_home_view_unauthenticated(self):
        response = self.client.get(reverse('blog:personal_home'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_post_single_view(self):
        response = self.client.get(reverse('blog:post_single', args=[self.post.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogtemplates/single.html')

    def test_post_search_view(self):
        response = self.client.get(reverse('blog:post_search'), {'q': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogtemplates/search.html')
        self.assertContains(response, 'Test Post')

    def test_add_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('blog:add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogtemplates/add.html')

    def test_add_view_unauthenticated(self):
        response = self.client.get(reverse('blog:add'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_edit_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('blog:edit', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogtemplates/edit.html')    
        
        
        
class TestPostModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.post = Post.newmanager.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            content='This is a test post body.',
            status=PUBLISHED
        )
        self.post.favourites.add(self.user)    
        self.post.save()
        self.post.refresh_from_db()

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.slug, 'test-post')
        self.assertEqual(self.post.author.username, 'testuser')
        self.assertEqual(self.post.content, 'This is a test post body.')
        self.assertEqual(self.post.status, PUBLISHED)
        self.assertIn(self.user, self.post.favourites.all())
        
        
