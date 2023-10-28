from django.urls import path
from .views import (
    AddListing,
    DeleteListing,
    EditListing,
    ListingDetails,
    ListingsView,
    product_list,
    SuccessView,
    CancelView,
    CreateStripeCheckoutSessionView,
    create_coinbase_checkout_session_view,
)

urlpatterns = [
    path("product_list/", product_list, name="product_list"),
    path("listings/", ListingsView.as_view(), name="listings"),
    path("listings/<int:pk>/", ListingDetails.as_view(), name="listing-details"),
    path("listings/add/", AddListing.as_view(), name="add-listing"),
    path("listings/<int:pk>/edit/", EditListing.as_view(), name="edit-listing"),
    path("listings/<int:pk>/delete/", DeleteListing.as_view(), name="delete-listing"),
    path(
        "create-checkout-session/<int:pk>/",
        CreateStripeCheckoutSessionView.as_view(),
        name="create-checkout-session",
    ),
    path("success/", SuccessView.as_view(), name="success"),
    path("cancel/", CancelView.as_view(), name="cancel"),
    path(
        "crypto-session/<int:id>/",
        create_coinbase_checkout_session_view,
        name="crypto-session",
    ),
]
