from django.views.generic import CreateView
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class UserRegisterView(CreateView):
    template_name = "authentication/register.html"
    model = UserModel
    fields = ["name", "email", "password", "is_business"]
