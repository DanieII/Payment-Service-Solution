from django.urls import path
from .views import (
    AddListing,
    ListingDetails,
    ListingsView,
    product_list,
    product_details,
)

urlpatterns = [
    path("product_list/", product_list, name="product_list"),
    path("product_details/<int:id>/", product_details, name="product_details"),
    path("listings/", ListingsView.as_view(), name="listings"),
    path("listings/<int:pk>/", ListingDetails.as_view(), name="listing-details"),
    path("listings/add/", AddListing.as_view(), name="add-listing"),
]
