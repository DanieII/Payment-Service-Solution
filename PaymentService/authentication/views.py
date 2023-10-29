from django.views.generic import CreateView
from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView, LogoutView, TemplateView
from django import forms
from django.urls import reverse_lazy
from common.mixins import AddPlaceholdersToFieldMixin
from .mixins import ProhibitLoggedUsersMixin
from .forms import CustomerUserRegisterForm, BusinessUserRegisterForm
from django.contrib.auth.hashers import make_password


UserModel = get_user_model()


class UserRegisterView(ProhibitLoggedUsersMixin, TemplateView):
    template_name = "authentication/register.html"


class BaseUserRegisterView(
    ProhibitLoggedUsersMixin, AddPlaceholdersToFieldMixin, CreateView
):
    template_name = "authentication/register-business.html"
    model = UserModel
    success_url = reverse_lazy("home")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["password"].widget = forms.PasswordInput(
            attrs={"placeholder": "Password"}
        )

        return form

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        is_business = self.request.POST.get("is_business", False)
        user.is_business = is_business
        print(self.request.POST)
        user.password = make_password(self.request.POST.get("password"))
        user.save()

        login(self.request, user)

        return response


class BusinessUserRegisterView(BaseUserRegisterView):
    template_name = "authentication/register-business.html"
    placeholders = {"name": "Company name", "email": "Email", "password": "Password"}
    form_class = BusinessUserRegisterForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["is_business"] = True

        return context_data


class CustomerUserRegisterView(BaseUserRegisterView):
    template_name = "authentication/register-customer.html"
    placeholders = {
        "name": "First and Last name",
        "email": "Email",
        "password": "Password",
    }
    form_class = CustomerUserRegisterForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["is_business"] = False

        return context_data


class UserLoginView(ProhibitLoggedUsersMixin, AddPlaceholdersToFieldMixin, LoginView):
    template_name = "authentication/login.html"
    placeholders = {"username": "Email", "password": "Password"}

    def get_success_url(self):
        return reverse_lazy("home")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["password"].widget = forms.PasswordInput(
            attrs={"placeholder": "Password"}
        )

        return form


class UserLogoutView(LogoutView):
    def get_success_url(self):
        return reverse_lazy("login")
