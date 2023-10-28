from django.shortcuts import redirect
from django.views.generic import ListView, TemplateView
from common.mixins import ProhibitBusinessUsersMixin, ProhibitCustomerUsersMixin
from products.models import Product
from django.contrib.auth import get_user_model
import stripe
from django.conf import settings
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from products.models import Order, Product


UserModel = get_user_model()


def redirect_to_correct_interface_view(request):
    if request.user.is_business:
        return redirect("business-home")
    return redirect("customer-home")


class BusinessUserHomeView(ProhibitCustomerUsersMixin, TemplateView):
    template_name = "common/business-home.html"


class CustomerUserHomeView(ProhibitBusinessUsersMixin, ListView):
    template_name = "common/customer-home.html"
    context_object_name = "products"
    paginate_by = 5

    def get_queryset(self):
        users = UserModel.objects.all()

        # Search item
        user = self.request.GET.get("user")
        if user:
            users = users.filter(name__icontains=user)

        products = Product.objects.filter(user__in=users)

        return products


class HomeView(TemplateView):
    template_name = "common/index.html"


@method_decorator(csrf_exempt, name="dispatch")
class StripeWebhookView(View):
    """
    Stripe webhook view to handle checkout session completed event.
    On successful event, creates an order in the database
    """

    def post(self, request, format=None):
        payload = request.body
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
        event = None

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse(status=400)

        # on successful event, create an order in the database
        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            customer_name = session["customer_details"]["name"]
            customer_email = session["customer_details"]["email"]
            product = Product.objects.get(id=session["metadata"]["product_id"])
            Order.objects.create(
                customer_name=customer_name,
                customer_email=customer_email,
                product_name=product.name,
                product_price=product.price,
            )
        return HttpResponse(status=200)
