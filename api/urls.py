from django.urls import include, path
from rest_framework import routers
from .views import UserViewSet,PostViewSet,ProfileViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)
router.register(r'profiles',ProfileViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    # Djoser endpoints 
    path("auth/", include("djoser.urls")), path("auth/", include("djoser.urls.authtoken")),
]
