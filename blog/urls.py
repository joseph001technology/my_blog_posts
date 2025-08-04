from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('add/', views.AddView.as_view(), name='add'),
    path('home/', views.personal_home, name='personal_home'),
    path('search/', views.post_search, name='post_search'),
    path('', views.home, name='homepage'),
    path('<slug:slug>/', views.post_single, name='post_single'),  # use slug consistently
    path('edit/<int:pk>/',views.EditView.as_view(),name='edit'),
    path('delete/<int:pk>',views.Delete.as_view(),name='delete'),
]
