from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import stripe
from .models import Product
from django.views.generic import ListView
from common.mixins import ProhibitCustomerUsersMixin

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


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        print("**"*20)
        print(request.GET.get)
        print(request.GET.get('product_id'))
        print("**" * 20)
        product_id = request.GET.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        try:
            # Create a new Checkout Session for the order
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': product.name,
                        'quantity': 1,
                        'currency': 'usd',
                        'amount': int(product.price * 100),  # Convert price to cents
                    }
                ]
            )

            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})
          
    return render(
        request, "products/product_list.html", {"products": products, "users": users}
    )


class ListingsView(ProhibitCustomerUsersMixin, ListView):
    template_name = "products/listings.html"
    model = Product

    def get_queryset(self):
        all_listings = super().get_queryset()
        current_business_listings = all_listings.filter(user=self.request.user)

        return current_business_listings
