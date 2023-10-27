from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'is_business']
    list_filter = ['is_business']
    list_editable = ['is_business']
