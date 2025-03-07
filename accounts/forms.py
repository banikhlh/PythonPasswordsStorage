from django import forms

from .models import CustomUser


class CustomUserForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ("email",)

    def clean_password(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don`t match")
        return password2

    def save(self, commit=True):
        user = super(CustomUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class RecoveryPhraseForm(forms.Form):
    words = forms.CharField(widget=forms.Textarea)

    def clean_words(self):
        words = self.cleaned_data["words"].strip().split()
        if len(words) != 24:
            raise forms.ValidationError("Must provide exactly 24 words")
        return " ".join(words)
