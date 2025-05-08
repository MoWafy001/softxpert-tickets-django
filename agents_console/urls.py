from . import views
from django.urls import path

urlpatterns = [
    path('customers/', views.customer_views.CustomerViewSet.as_view(), name='customer-list'),
    path('customers/<int:customer_id>/', views.customer_views.CustomerByIdViewSet.as_view(), name='customer-detail'),
    path('tickets/', views.ticket_views.TicketViewSet.as_view(), name='tickets-list'),
    path('tickets/<int:ticket_id>/', views.ticket_views.TicketByIdViewSet.as_view(), name='ticket-detail'),
    path('tickets/<int:ticket_id>/sell/', views.ticket_views.SellTicketViewSet.as_view(), name='sell-ticket'),
]