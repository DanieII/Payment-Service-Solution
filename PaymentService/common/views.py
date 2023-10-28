from django.shortcuts import redirect
from django.views.generic import ListView, TemplateView
from common.mixins import ProhibitBusinessUsersMixin, ProhibitCustomerUsersMixin
from products.models import Product
from django.contrib.auth import get_user_model

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
