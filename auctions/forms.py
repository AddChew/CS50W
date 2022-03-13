from django import forms
from django.utils.translation import gettext_lazy as _
from .models import *


class CreateListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "desc", "start_price", "url", "categories"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control form-group"}),
            "desc": forms.Textarea(attrs={"class": "form-control form-group"}),
            "start_price": forms.NumberInput(attrs={"class": "form-control form-group", "step": 0.01, "min": 0.00}),
            "url": forms.TextInput(attrs={"class": "form-control form-group"}),
            "categories": forms.SelectMultiple(attrs={"class": "form-control form-group"}),
        }
        labels = {
            "desc": _("Description"),
            "start_price": _("Start Price"),
            "url": _("Image URL"),
        }


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["price"]
        widgets = {
            "price": forms.NumberInput(attrs={"class": "form-control form-group", "step": 0.01, "min": 0.00, "placeholder": "Bid"}),
        }
        labels = {
            "price": _(""),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["post"]
        widgets = {
            "post": forms.Textarea(attrs={"class": "form-control form-group", "placeholder": "Write a comment...", "rows": 5}),
        }
        labels = {
            "post": _(""),
        }


class ButtonForm(forms.Form):
    btn = forms.CharField()