from django.urls import path
from .views import (
    UserLoginView,
    UserLogoutView,
    UserRegisterView,
    BusinessUserRegisterView,
    CustomerUserRegisterView,
)

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path(
        "register/business",
        BusinessUserRegisterView.as_view(),
        name="register_business",
    ),
    path(
        "register/customer",
        CustomerUserRegisterView.as_view(),
        name="register_customer",
    ),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
]
