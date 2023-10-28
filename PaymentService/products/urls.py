from django.urls import path
from .views import (
    AddListing,
    ListingDetails,
    ListingsView,
    product_list,
    product_details,
    SuccessView, CancelView,
    CreateStripeCheckoutSessionView,
    create_coinbase_checkout_session_view,
)

urlpatterns = [
    path("product_list/", product_list, name="product_list"),
    path("product_details/<int:id>/", product_details, name="product_details"),
    path("listings/", ListingsView.as_view(), name="listings"),
    path("listings/<int:pk>/", ListingDetails.as_view(), name="listing-details"),
    path("listings/add/", AddListing.as_view(), name="add-listing"),
    path("create-checkout-session/<int:pk>/", CreateStripeCheckoutSessionView.as_view(),
         name="create-checkout-session"),
    path("success/", SuccessView.as_view(), name="success"),
    path("cancel/", CancelView.as_view(), name="cancel"),
    path('crypto-session/<int:id>/', create_coinbase_checkout_session_view, name='crypto-session'),
]
