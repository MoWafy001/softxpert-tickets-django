from . import views
from django.urls import path

urlpatterns = [
    path('customers/', views.customer_views.CustomerViewSet.as_view(), name='customer-list'),
    path('customers/<int:customer_id>/', views.customer_views.CustomerByIdViewSet.as_view(), name='customer-detail'),
]