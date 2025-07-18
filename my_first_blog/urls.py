from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, RedirectView
from blog import views

urlpatterns = [
     path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),   # Home
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # 🔐 Social login
    path('blog/', include(('blog.urls', 'blog'), namespace='blog')),
    path('logout-success/', views.logout_success, name='logout_success'),# Blog app
     path('home/', login_required(views.personal_home), name='personal_home'),  
]
