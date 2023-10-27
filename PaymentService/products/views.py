from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Product
from django.contrib.auth import get_user_model

UserModel = get_user_model()


# Create your views here.
def product_list(request):
    users = UserModel.objects.all()

    # search item
    user = request.GET.get('user')
    if user != '' and user is not None:
        users = users.filter(name__icontains=user)

    products = []
    for u in users:
        products.extend(Product.objects.filter(user=u))

    # pagination
    paginator = Paginator(products, 2)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    return render(request, 'products/product_list.html', {'products': products, 'users': users})
