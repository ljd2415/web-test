from django.urls import path

from .views import pi_collection

urlpatterns = [
    path('pi/', pi_collection, name='pi_collection'),
]
