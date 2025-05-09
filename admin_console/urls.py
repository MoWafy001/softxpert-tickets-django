from . import views
from django.urls import path

app_name = "agents-console"

urlpatterns = [
    path("customers/", views.customer_views.CustomerViewSet.as_view(), name="customers"),
    path("customers/<int:customer_id>/", views.customer_views.CustomerByIdViewSet.as_view(), name="customer-by-id"),
    path("tickets/", views.ticket_views.TicketViewSet.as_view(), name="tickets"),
    path("tickets/<int:ticket_id>/", views.ticket_views.TicketByIdViewSet.as_view(), name="ticket-by-id"),
]