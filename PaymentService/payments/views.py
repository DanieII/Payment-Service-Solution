from django.shortcuts import render
from django.views.generic import TemplateView
import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.views import View


#
# from .models import Price

# Create your views here.
class ButtonView(TemplateView):
    # this class is only to show the button on the screen
    template_name = 'payments/home.html'


# getting the key from settings.py
stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateStripeCheckoutSessionView(View):
    """
    Create a checkout session and redirect the user to Stripe's checkout page
    """

    def post(self, request, *args, **kwargs):
        # price = Price.objects.get(id=self.kwargs["pk"])

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": 23.00,
                        "product_data": {
                            "name": "Plumer Service",
                            "description": "No description at this time",
                            "images": [
                                # f"{settings.BACKEND_DOMAIN}/{price.product.thumbnail}"
                            ],
                        },
                    },
                    "quantity": 1,
                }
            ],
            metadata={"product_id": 1},
            mode="payment",
            success_url=settings.PAYMENT_SUCCESS_URL,
            cancel_url=settings.PAYMENT_CANCEL_URL,
        )
        return redirect(checkout_session.url)
