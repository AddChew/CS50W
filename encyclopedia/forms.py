from django import forms
from django.core.exceptions import ValidationError
from . import util


class EditEntry(forms.Form):
    content = forms.CharField(
        label="Content", 
        widget=forms.Textarea(attrs={
            "class": "form-control"
        }), 
        required=True
        )    


class NewEntry(EditEntry):
            
    title = forms.CharField(
        label="Title", 
        widget=forms.TextInput(attrs={
            "class": "form-control"
        }),
        required=True,
        )

    def clean(self):
        super().clean()
        title = self.cleaned_data.get("title")

        if title in util.list_entries():
            raise ValidationError(
                "A page with the title: %(title)s already exists.",
                code="invalid",  
                params={"title": title}
                )