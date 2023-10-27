from django.views.generic import CreateView
from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView
from django import forms
from django.urls import reverse_lazy
from common.mixins import AddPlaceholdersToFieldMixin


UserModel = get_user_model()


class UserRegisterView(
    AddPlaceholdersToFieldMixin,
    CreateView,
):
    template_name = "authentication/register.html"
    model = UserModel
    fields = ["name", "email", "password", "is_business"]
    placeholders = {"name": "Name", "email": "Email", "password": "Password"}
    success_url = reverse_lazy("home")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["is_business"].label = "Business Account?"
        form.fields["password"].widget = forms.PasswordInput(
            attrs={"placeholder": "Password"}
        )

        return form

    def form_valid(self, form):
        response = super().form_valid(form)
        self.validate_business_name(form)
        user = form.save()

        login(self.request, user)

        return response

    def validate_business_name(self, form):
        if not form.cleaned_data.get("is_business"):
            return

        business_name = form.cleaned_data.get("name")
        business_name_taken = UserModel.objects.filter(name=business_name).exists()

        if business_name_taken:
            raise forms.ValidationError("This Business name is already taken.")


class UserLoginView(AddPlaceholdersToFieldMixin, LoginView):
    template_name = "authentication/login.html"
