from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class CustomLoginForm(AuthenticationForm):
    name = forms.CharField()

    def clean(self):
        name = self.cleaned_data.get("name")
        # if not UserModel.objects.
        return super().clean()
