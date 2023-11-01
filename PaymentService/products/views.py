from django.core.paginator import Paginator
from django.shortcuts import reverse
from django.views.generic import (
    DeleteView,
    UpdateView,
)
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, TemplateView
from .models import Product
from django.contrib.auth import get_user_model
from common.mixins import (
    ProhibitBusinessUsersMixin,
    ProhibitCustomerUsersMixin,
    AddPlaceholdersToFieldMixin,
)
from django import forms
from django.conf import settings
import stripe
from coinbase_commerce.client import Client
from .mixins import CheckForObjectOwnerMixin

UserModel = get_user_model()
stripe.api_key = settings.STRIPE_SECRET_KEY


class ListingsView(ProhibitCustomerUsersMixin, ListView):
    template_name = "products/listings.html"
    model = Product

    def get_queryset(self):
        all_listings = super().get_queryset()
        current_business_listings = all_listings.filter(user=self.request.user)

        return current_business_listings


class AddListing(ProhibitCustomerUsersMixin, AddPlaceholdersToFieldMixin, CreateView):
    model = Product
    template_name = "products/add-listing.html"
    fields = ["name", "description", "price", "media"]
    placeholders = {"name": "Name", "description": "Description", "price": "Price"}
    success_url = reverse_lazy("listings")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["description"].widget = forms.Textarea(
            attrs={"placeholder": "Description"}
        )

        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)

        return response


class ListingDetails(DetailView):
    model = Product

    def get(self, request, *args, **kwargs):
        # increments product views for current object
        self.object = self.get_object()
        self.object.visits_count += 1
        self.object.save()
        return super().get(request, *args, **kwargs)

    template_name = "products/listing-details.html"


class EditListing(ProhibitCustomerUsersMixin, CheckForObjectOwnerMixin, UpdateView):
    model = Product
    template_name = "products/edit-listing.html"
    fields = ["name", "description", "price", "media"]

    def get_success_url(self):
        pk = self.object.pk
        return reverse("listing-details", kwargs={"pk": pk})


class DeleteListing(ProhibitCustomerUsersMixin, CheckForObjectOwnerMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("listings")


class CreateStripeCheckoutSessionView(ProhibitBusinessUsersMixin, View):
    """
    Create a checkout session and redirect the user to Stripe's checkout page
    """

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(id=self.kwargs["pk"])

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": int(product.price) * 100,
                        "product_data": {
                            "name": product.name,
                            "description": product.description,
                        },
                    },
                    "quantity": 1,
                }
            ],
            metadata={"product_id": product.id},
            mode="payment",
            success_url=settings.PAYMENT_SUCCESS_URL,
            cancel_url=settings.PAYMENT_CANCEL_URL,
        )
        return redirect(checkout_session.url)


class SuccessView(TemplateView):
    template_name = "products/payment_success.html"


class CancelView(TemplateView):
    template_name = "products/payment_failed.html"


def create_coinbase_checkout_session_view(request, id):
    if request.user.is_business:
        return redirect("business-home")

    current_order = Product.objects.get(id=id)
    client = Client(api_key=settings.COINBASE_COMMERCE_API_KEY)
    domain_url = settings.BACKEND_DOMAIN
    product = {
        "name": current_order.name,
        "description": current_order.description,
        "local_price": {"amount": str(current_order.price), "currency": "USD"},
        "pricing_type": "fixed_price",
        "redirect_url": settings.PAYMENT_SUCCESS_URL,
        "cancel_url": settings.PAYMENT_CANCEL_URL,
    }
    charge = client.charge.create(**product)
    return redirect(charge.hosted_url)


class BuyListingView(ProhibitBusinessUsersMixin, TemplateView):
    template_name = "products/buy-listing.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["listing_pk"] = self.kwargs.get("pk")
        return context_data
