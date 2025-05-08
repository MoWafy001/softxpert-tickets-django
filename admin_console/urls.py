from . import views
from django.urls import path

urlpatterns = [
    path("customers/", views.customer_views.list_customers_view, name="list_customers"),
]