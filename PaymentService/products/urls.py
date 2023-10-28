from django.urls import path
from .views import ListingsView, product_list
from . import views

urlpatterns = [
    path("product_list/", views.product_list, name="product_list"),
    path("product_details/<int:id>/", views.product_details, name="product_details"),
    path("config/", views.stripe_config, name="stripe_config"),
    path('create-checkout-session/', views.create_checkout_session, name='api_checkout_session'),
    path('success/', views.SuccessView.as_view()),  # new
    path('cancelled/', views.CancelledView.as_view()),  # new
    path("listings/", ListingsView.as_view(), name="listings"),
]