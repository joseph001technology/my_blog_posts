from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
     path('home/', views.personal_home, name='personal_home'),
    path('', views.home, name='homepage'),
    path('<slug:slug>/', views.post_single, name='post_single'),  # use slug consistently
     
]
