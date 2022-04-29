from django import forms
from django.utils.translation import gettext_lazy as _
from .models import User, Post


class LoginForm(forms.Form):
    username = forms.CharField(label = "", widget = forms.TextInput(attrs={"class": "form-control form-group", "placeholder": "Username"}))
    password = forms.CharField(label = "", widget = forms.PasswordInput(attrs={"class": "form-control form-group", "placeholder": "Password"}))


class RegisterForm(forms.Form):
    username = forms.CharField(label = "", widget = forms.TextInput(attrs={"class": "form-control form-group", "placeholder": "Username"}))
    email = forms.EmailField(label = "", widget = forms.EmailInput(attrs={"class": "form-control form-group", "placeholder": "Email Address"}))
    password = forms.CharField(label = "", widget = forms.PasswordInput(attrs={"class": "form-control form-group", "placeholder": "Password"}))
    confirmation = forms.CharField(label = "", widget = forms.PasswordInput(attrs={"class": "form-control form-group", "placeholder": "Confirm Password"}))

    def clean_username(self):

        # Retrieve username field
        username = self.cleaned_data.get("username")

        # Check if username already exists
        try:
            User.objects.get(username = username)
            raise forms.ValidationError(
                _("Username %(username)s already taken."),
                code = "invalid",
                params = {"username": username}
            )

        except User.DoesNotExist:
            return username

    def clean(self):

        # Retrieve cleaned data
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmation = cleaned_data.get("confirmation")

        # Ensure that password matches confirmation
        if password != confirmation:
            raise forms.ValidationError(
                _("Passwords must match."),
                code = "invalid",
            )


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