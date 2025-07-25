from django import forms
from .models import Post,Comment
from allauth.socialaccount.forms import SignupForm


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['slug'].required = False 
        

class MyCustomSocialSignupForm(SignupForm):
    full_name = forms.CharField(max_length=100, label="Full Name")

    def save(self, request):
        user = super().save(request)
        user.full_name = self.cleaned_data['full_name']  # If you have this field
        user.save()
        return user



class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)  # Only let users write comment content
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }
