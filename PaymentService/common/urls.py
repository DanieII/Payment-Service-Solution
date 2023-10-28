from django.urls import path
from .views import HomeView, StripeWebhookView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("webhooks/stripe/", StripeWebhookView.as_view(), name="stripe-webhook"),
]
