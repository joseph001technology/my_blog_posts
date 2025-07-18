from django import forms
from .models import Post
from allauth.socialaccount.forms import SignupForm


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'

class MyCustomSocialSignupForm(SignupForm):
    full_name = forms.CharField(max_length=100, label="Full Name")

    def save(self, request):
        user = super().save(request)
        user.full_name = self.cleaned_data['full_name']  # If you have this field
        user.save()
        return user


