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