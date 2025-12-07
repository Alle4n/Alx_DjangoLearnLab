from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Post, Comment
from taggit.forms import TagWidget  # <-- add for tagging support

# ================================
# USER REGISTRATION FORM
# ================================
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

# ================================
# POST FORM (with Tags)
# ================================
class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "tags"]  # include tags field
        widgets = {
            "tags": TagWidget(attrs={'placeholder': 'Add tags separated by commas'})
        }

# ================================
# COMMENT FORM
# ================================
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment here...'})
        }
