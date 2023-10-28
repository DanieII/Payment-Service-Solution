from django.urls import path
from .views import AddListing, ListingDetails, ListingsView, product_list
from . import views

urlpatterns = [
    path("product_list/", views.product_list, name="product_list"),
    path("product_details/<int:id>/", views.product_details, name="product_details"),
    path("config/", views.stripe_config, name="stripe_config"),
    path('create-checkout-session/', views.create_checkout_session, name='api_checkout_session'),
    path('success/', views.SuccessView.as_view()),  # new
    path('cancelled/', views.CancelledView.as_view()),  # new
    path("listings/", ListingsView.as_view(), name="listings"),
    path("listings/<int:pk>/", ListingDetails.as_view(), name="listing-details"),
    path("listings/add/", AddListing.as_view(), name="add-listing"),
]
