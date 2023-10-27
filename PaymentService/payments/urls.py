from django.urls import path
from . import views

urlpatterns = [
    path('', views.ButtonView.as_view(), name='test-payments'),
    ]