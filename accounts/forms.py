from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Blog
from .models import BlogPost


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = [
            'title'
        ]


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = [
            'title',
            'body'
        ]
