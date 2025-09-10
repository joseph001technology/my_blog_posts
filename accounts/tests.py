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
        
        
        
class userProfileTestCase(APITestCase):
    def setUp(self):
        # create a new user making a post request to djoser endpoint
        self.user = self.client.post('/api/auth/users/',  data = {
        "username": "testuser1",
        "email": "testuser1@josek.com",
        "password": "testpassword123"
      }) 
        # obtain an auth token for the newly created user
        response = self.client.post(
         '/api/auth/jwt/create/', 
        data={'email': 'testuser1@josek.com', 'password': 'testpassword123'}
          )
        self.token = response.data['access']  # <-- not 'auth_token'

        self.api_authentication()
     
    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        
   
      
    def test_user_profile_create(self):
        response = self.client.post(reverse('userauth:edit'), data={
            'bio': 'This is a test bio',
            'avatar': None  # or provide a test image if your model requires it
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)     
          
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
