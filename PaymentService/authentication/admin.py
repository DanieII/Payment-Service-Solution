from django.contrib import admin
from .models import CustomUser
from django.contrib.auth import get_user_model

UserModel = get_user_model()


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "is_business"]
    list_filter = ["is_business"]
    list_editable = ["is_business"]
