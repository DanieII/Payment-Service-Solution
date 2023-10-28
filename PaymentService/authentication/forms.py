from django import forms
from django.contrib.auth import get_user_model
from .validators import (
    validate_customer_name_length,
    validate_customer_name_for_only_letters,
    validate_business_name_for_distinctiveness,
)

UserModel = get_user_model()


class BaseUserRegisterForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ["name", "email", "password"]


class BusinessUserRegisterForm(BaseUserRegisterForm):
    def clean_name(self):
        name = self.cleaned_data.get("name")

        validate_business_name_for_distinctiveness(name)

        return name


class CustomerUserRegisterForm(BaseUserRegisterForm):
    def clean_name(self):
        name = self.cleaned_data.get("name")

        validate_customer_name_length(name)
        validate_customer_name_for_only_letters(name)

        return name
