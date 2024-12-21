import re

from django import forms

from .models import PasswordEntry


class PasswordEntryForm(forms.ModelForm):
    class Meta:
        model = PasswordEntry
        fields = ["website", "username", "email", "password"]
        widgets = {
            "password": forms.PasswordInput(),
        }

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", password):
            raise forms.ValidationError(
                "Password must contain at least one uppercase letter"
            )
        if not re.search(r"[a-z]", password):
            raise forms.ValidationError(
                "Password must contain at least one lowercase letter"
            )
        if not re.search(r"\d", password):
            raise forms.ValidationError("Password must contain at least one number")
        if not re.search(r"[ !@#$%&'()*+,-./[\\\]^_`{|}~" + r'"]', password):
            raise forms.ValidationError(
                "Password must contain at least one special character"
            )
        return password
