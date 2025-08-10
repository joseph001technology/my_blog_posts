from django import forms
from .models import Post,Comment
from allauth.socialaccount.forms import SignupForm
from mptt.forms import TreeNodeChoiceField
from django_summernote.widgets import SummernoteWidget

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
    parent = TreeNodeChoiceField(
        queryset=Comment.objects.all(),
        required=False,
        widget=forms.CharField(widget=SummernoteWidget())
    )

    class Meta:
        model = Comment
        fields = ('parent', 'content')
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].label = ''
        
        
 

class PostSearchForm(forms.Form):
    q = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['q'].label = 'Search For'
        self.fields['q'].widget.attrs.update(
            {'class': 'form-control'})

               