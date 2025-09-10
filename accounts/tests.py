from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.test import TestCase


# Create your tests here.

User = get_user_model()

class RegistrationTestCase(APITestCase):
    def test_user_registration(self):
        data = {
        "username": "testuser",
        "email": "testuser@josek.com",
        "password": "PASwword1234"
    }
        response = self.client.post('/api/auth/users/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, "testuser")
        
        
        
class UserProfileTestCase(TestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create_user(
            username="testuser1",
            email="testuser1@josek.com",
            password="testpassword123"
        )
        # Log in user with Django’s test client (session auth)
        self.client.login(username="testuser1", password="testpassword123")

    def test_user_profile_create(self):
        response = self.client.post(reverse('userauth:edit'), {
            'bio': 'This is a test bio',
            'avatar': ''  # empty string allowed
        })
        self.assertEqual(response.status_code, 200)
          
          
          
class TestUserModel(TestCase):
  def test_create_user(self):
      user = User.objects.create_user(username='testuser',password="password")   
      self.assertEqual(user.username, 'testuser')
      self.assertTrue(user.check_password('password'))
      
  def test_update_user(self):
      user = User.objects.create_user(username='testuser',password="password")   
      self.assertEqual(user.username, 'testuser')
      self.assertTrue(user.check_password('password'))
      
      user.username = 'updateduser'
      user.set_password('newpassword')
      user.save()
      self.assertEqual(user.username, 'updateduser')
      self.assertTrue(user.check_password('newpassword'))
      
      


class TestAccountUrls(TestCase):
    def test_register_url(self):
        url = reverse('userauth:custom_signup')
        self.assertEqual(url, '/user/signup/')
        
    def test_profile_url(self):
        url = reverse('userauth:profile')
        self.assertEqual(url, '/user/profile/')
        
    def test_edit_url(self):
        url = reverse('userauth:edit')
        self.assertEqual(url, '/user/profile/edit/')
        
    def test_favourite_add_url(self):
        url = reverse('userauth:favourite_add', args=[1])
        self.assertEqual(url, '/user/fav/1/')
        
    def test_favourite_list_url(self):
        url = reverse('userauth:favourite_list')
        self.assertEqual(url, '/user/profile/favourites/')
        
    def test_delete_user_url(self):
        url = reverse('userauth:deleteuser')
        self.assertEqual(url, '/user/profile/delete/')
