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
    media = models.ImageField(upload_to="images", blank=True)

    def __str__(self):
        return self.name
