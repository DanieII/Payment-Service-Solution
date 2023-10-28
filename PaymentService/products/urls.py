from django.urls import path
from .views import ListingsView, product_list

urlpatterns = [
    path("product_list/", product_list, name="product_list"),
    path("listings/", ListingsView.as_view(), name="listings"),
]
