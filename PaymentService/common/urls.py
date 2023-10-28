from django.urls import path
from .views import (
    BusinessUserHomeView,
    CustomerUserHomeView,
    redirect_to_correct_interface_view,
    StripeWebhookView,
)

urlpatterns = [
    path("", redirect_to_correct_interface_view, name="home"),
    path("business/", BusinessUserHomeView.as_view(), name="business-home"),
    path("customer/", CustomerUserHomeView.as_view(), name="customer-home"),
    path("webhooks/stripe/", StripeWebhookView.as_view(), name="stripe-webhook"),
]
