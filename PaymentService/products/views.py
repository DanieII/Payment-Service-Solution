from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from .models import Product
from django.contrib.auth import get_user_model
from common.mixins import ProhibitCustomerUsersMixin, AddPlaceholdersToFieldMixin
from django import forms
from django.views.generic import TemplateView
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import stripe

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
