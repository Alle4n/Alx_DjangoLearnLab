from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Post, Comment
from taggit.forms import TagWidget  # <-- required for tagging

# ================================
# USER REGISTRATION FORM
# ================================
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

# ================================
# POST FORM (with tagging)
# ================================
class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'video_URL', 'content_text', 'score', 'tags']
        widgets = {
            'content_text': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
            'tags': TagWidget(),  # <-- Tag input widget
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
