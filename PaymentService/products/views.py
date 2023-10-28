from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, TemplateView
from .models import Product
from django.contrib.auth import get_user_model
from common.mixins import ProhibitCustomerUsersMixin, AddPlaceholdersToFieldMixin
from django import forms
from django.conf import settings
import stripe
from coinbase_commerce.client import Client

UserModel = get_user_model()


# Create your views here.
def product_list(request):
    users = UserModel.objects.all()

    # search item
    user = request.GET.get('user')
    if user != '' and user is not None:
        # TODO: check if this isn't making any problems
        users = users.filter(name__icontains=user)

    products = []
    for u in users:
        products.extend(Product.objects.filter(user=u))

    # pagination
    paginator = Paginator(products, 2)
    page = request.GET.get("page")
    products = paginator.get_page(page)

    return render(request, 'products/product_list.html', {'products': products, 'users': users})


def product_details(request, id):
    product = Product.objects.get(id=id)
    stripe_publishable_key = settings.STRIPE_PUBLISHABLE_KEY
    context = {
        'product': product,
        'stripe_publishable_key': stripe_publishable_key
    }
    return render(request, 'products/product_details.html', context)


stripe.api_key = settings.STRIPE_SECRET_KEY


class ListingsView(ProhibitCustomerUsersMixin, ListView):
    template_name = "products/listings.html"
    model = Product

    def get_queryset(self):
        all_listings = super().get_queryset()
        current_business_listings = all_listings.filter(user=self.request.user)

        return current_business_listings


class AddListing(AddPlaceholdersToFieldMixin, CreateView):
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
    template_name = "products/listing-details.html"


stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateStripeCheckoutSessionView(View):
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
    current_order = Product.objects.get(id=id)
    client = Client(api_key=settings.COINBASE_COMMERCE_API_KEY)
    domain_url = settings.BACKEND_DOMAIN
    product = {
        'name': current_order.name,
        'description': current_order.description,
        'local_price': {'amount': str(current_order.price), 'currency': 'USD'},
        'pricing_type': 'fixed_price',
        'redirect_url': settings.PAYMENT_SUCCESS_URL,
        'cancel_url': settings.PAYMENT_CANCEL_URL,
    }
    charge = client.charge.create(**product)
    return render(request, 'products/product_details.html', {'charge': charge})
