from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="products"
    )
    media = models.ImageField(upload_to="images")
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    product_name = models.CharField(max_length=100)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer_email} - {self.product_name}"
