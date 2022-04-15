from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"class": "form-control form-group", "placeholder": "What's happening?"}),
        }
        labels = {
            "content": _("")
        }