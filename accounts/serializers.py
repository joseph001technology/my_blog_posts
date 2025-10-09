# accounts/serializers.py
from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  
    # or serializers.PrimaryKeyRelatedField if you prefer IDs

    class Meta:
        model = Profile
        fields = ["id", "user", "avatar", "bio"]
        read_only_fields = ["id", "user"]
        
        
        
# from rest_framework import serializers
# from .models import Profile
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'user_name', 'email', 'first_name']

# class ProfileSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)

#     class Meta:
#         model = Profile
#         fields = ["id", "user", "avatar", "bio"]
#         read_only_fields = ["id", "user"]
