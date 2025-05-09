from common.json_responses import DataJsonResponse, ErrorJsonResponse
from customers.models import Customer
from tickets.models import Ticket
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from common.csrf_except_session_authentication import CsrfExemptSessionAuthentication
from users.permissions import IsAgent
from django.db import transaction, DatabaseError
import time


class TicketViewSet(APIView):
    """
    ViewSet for managing tickets.
    """

    authentication_classes = (CsrfExemptSessionAuthentication, SessionAuthentication)
    permission_classes = [IsAuthenticated, IsAgent]
        
    
    @action(detail=False, methods=["get"])
    def get(self, request):
        """
        List all tickets.
        """

        user = request.user
        if not user.is_authenticated:
            return ErrorJsonResponse("User not authenticated", status=401)

        # retry incase of database error because of deadlock
        started_at = time.time()
        def get_time_elapsed():
            return time.time() - started_at
        while get_time_elapsed() < 5:
            try:
                with transaction.atomic():
                    no_tickets_assigned_to_agent = Ticket.objects.filter(assigned_to=user).count()
                    no_tickets_to_assign = 15 - no_tickets_assigned_to_agent
                    if no_tickets_to_assign > 0:
                        unassigned_tickets = (
                            Ticket.objects.filter(assigned_to=None)
                            .order_by("created_at")
                            .select_for_update(
                                skip_locked=True
                            )[:no_tickets_to_assign]
                        )
                        for ticket in unassigned_tickets:
                            ticket.assigned_to = user
                            ticket.save()

                # Retrieve all tickets assigned to the user
                tickets = Ticket.objects.filter(assigned_to=user).order_by("created_at")
                tickets_list = [
                    {
                        "id": ticket.id,
                        "title": ticket.title,
                        "description": ticket.description,
                        "created_at": ticket.created_at,
                        "updated_at": ticket.updated_at,
                    }
                    for ticket in tickets
                ]
                return DataJsonResponse(tickets_list)

            except DatabaseError as e:
                print(f"Database error: {e}. Retrying...")
                time.sleep(1)  # Wait before retrying

        return ErrorJsonResponse("Could not assign tickets due to a database error", status=500)


class TicketByIdViewSet(APIView):
    """
    ViewSet for managing tickets by ID.
    """

    authentication_classes = (CsrfExemptSessionAuthentication, SessionAuthentication)
    permission_classes = [IsAuthenticated, IsAgent]

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
                "created_at": ticket.created_at,
                "updated_at": ticket.updated_at,
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
    permission_classes = [IsAuthenticated, IsAgent]

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