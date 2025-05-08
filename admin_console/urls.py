from . import views
from django.urls import path

urlpatterns = [
    path("customers/", views.customer_views.CustomerViewSet.as_view()),
    path("customers/<int:customer_id>/", views.customer_views.CustomerByIdViewSet.as_view()),
    path("tickets/", views.ticket_views.TicketViewSet.as_view()),
    path("tickets/<int:ticket_id>/", views.ticket_views.TicketByIdViewSet.as_view()),
]