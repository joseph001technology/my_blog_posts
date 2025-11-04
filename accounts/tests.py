from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.

User = get_user_model()

class RegistrationTestCase(APITestCase):
    def test_user_registration(self):
        data = {
        "user_name": "testuser",
        "email": "testuser@josek.com",
        "password": "PASwword1234",
        "first_name": "Test",
        
    }
        response = self.client.post('/api/auth/users/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().user_name, "testuser")
        
        
        
class UserProfileTestCase(TestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create_user(
            user_name="testuser1",
            email="testuser1@josek.com",
            password="testpassword123",
            first_name="Test",
            
        )
        # Log in user with Django’s test client (session auth)
        self.client.login(user_name="testuser1", password="testpassword123")

    def test_user_profile_create(self):
        response = self.client.post(reverse('userauth:edit'), {
            # UserEditForm fields
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser1@josek.com',
            
            # UserProfileForm fields
            'bio': 'This is a test bio',
            'avatar': ''  # empty string allowed
        })
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.profile.bio, 'This is a test bio')
  
          
          
class TestUserModel(TestCase):
  def test_create_user(self):
      user = User.objects.create_user(user_name='testuser',password="password", first_name="Test", email="testuser@example.com")   
      self.assertEqual(user.user_name, 'testuser')
      self.assertTrue(user.check_password('password'))
      
  def test_update_user(self):
      user = User.objects.create_user(user_name='testuser',password="password", first_name="Test", email="testuser@example.com")   
      self.assertEqual(user.user_name, 'testuser')
      self.assertTrue(user.check_password('password'))
      self.assertEqual(user.first_name, 'Test')
      
      user.user_name = 'updateduser'
      user.set_password('newpassword')
      user.save()
      self.assertEqual(user.user_name, 'updateduser')
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
