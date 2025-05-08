from common.json_responses import DataJsonResponse, ErrorJsonResponse
from customers.models import Customer
from tickets.models import Ticket
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from common.csrf_except_session_authentication import CsrfExemptSessionAuthentication


class TicketViewSet(APIView):
    """
    ViewSet for managing tickets.
    """

    authentication_classes = (CsrfExemptSessionAuthentication, SessionAuthentication)
    permission_classes = [IsAuthenticated]
        
    
    @action(detail=False, methods=["get"])
    def get(self, request):
        """
        List all tickets.
        """
        user = request.user
        if not user.is_authenticated:
            return ErrorJsonResponse("User not authenticated", status=401)

        no_tickets_assigned_to_agent = Ticket.objects.filter(assigned_to=user).count()
        no_tickets_to_assign = 15 - no_tickets_assigned_to_agent
        if no_tickets_to_assign > 0:
            ids = Ticket.objects.filter(assigned_to=None).order_by("created_at").values_list("id", flat=True)[:no_tickets_to_assign]
            Ticket.objects.filter(id__in=ids).update(assigned_to=user)
        tickets = Ticket.objects.filter(assigned_to=user).order_by("created_at")
        tickets_list = [
            {
                "id": ticket.id,
                "title": ticket.title,
                "description": ticket.description,
            }
            for ticket in tickets
        ]
        return DataJsonResponse(tickets_list)


class TicketByIdViewSet(APIView):
    """
    ViewSet for managing tickets by ID.
    """

    authentication_classes = (CsrfExemptSessionAuthentication, SessionAuthentication)
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"])
    def get(self, request, ticket_id=None):
        """
        Retrieve a ticket by ID.
        """
        user = request.user
        if not user.is_authenticated:
            return ErrorJsonResponse("User not authenticated", status=401)
        try:
            ticket = Ticket.objects.get(pk=ticket_id, assigned_to=user)
            ticket_data = {
                "id": ticket.id,
                "title": ticket.title,
                "description": ticket.description,
            }
            return DataJsonResponse(ticket_data)

        except Ticket.DoesNotExist:
            return ErrorJsonResponse("Ticket not found", status=404)
        except Exception as e:
            return ErrorJsonResponse(str(e), status=500)


class SellTicketViewSet(APIView):
    """
    ViewSet for managing tickets by ID.
    """

    authentication_classes = (CsrfExemptSessionAuthentication, SessionAuthentication)
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"])
    def post(self, request, ticket_id=None):
        """
        Sell a ticket to a customer
        """
        user = request.user
        if not user.is_authenticated:
            return ErrorJsonResponse("User not authenticated", status=401)
        try:
            ticket = Ticket.objects.get(pk=ticket_id, assigned_to=user)
            if ticket.sold_to is not None:
                return ErrorJsonResponse("Ticket already sold", status=400)

            customer_id = request.data.get("customer_id")
            customer = Customer.objects.get(pk=customer_id)
            ticket.sold_to = customer
            ticket.assigned_to = None
            ticket.save()
            return DataJsonResponse({"message": "Ticket sold successfully"})

        except Ticket.DoesNotExist:
            return ErrorJsonResponse("Ticket not found", status=404)
        except Customer.DoesNotExist:
            return ErrorJsonResponse("Customer not found", status=404)
        except Exception as e:
            return ErrorJsonResponse(str(e), status=500)