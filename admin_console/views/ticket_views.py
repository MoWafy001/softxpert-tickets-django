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

    @action(detail=False, methods=["post"])
    def post(self, request):
        """
        Create a new ticket.
        """
        if request.method != "POST":
            return ErrorJsonResponse("Invalid request method", status=405)

        user = request.user
        if not user.is_authenticated:
            return ErrorJsonResponse("User not authenticated", status=401)

        try:
            data = request.data
            title = data.get("title")
            description = data.get("description")

            if not title or not description:
                return ErrorJsonResponse({"error": "title and description are required"}, status=400)

            ticket = Ticket.objects.create(title=title, description=description, created_by=user)
            return DataJsonResponse({"message": "Ticket created successfully", "ticket_id": ticket.id}, status=201)

        except Exception as e:
            return ErrorJsonResponse(str(e), status=500)
        
    
    @action(detail=False, methods=["get"])
    def get(self, request):
        """
        List all tickets.
        """
        tickets = Ticket.objects.all()
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
        try:
            ticket = Ticket.objects.get(pk=ticket_id)
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

    @action(detail=True, methods=["patch"])
    def patch(self, request, ticket_id=None):
        """
        Update a ticket by ID.
        """
        try:
            ticket = Ticket.objects.get(pk=ticket_id)
            data = request.data

            if "title" in data:
                ticket.title = data["title"]
            if "description" in data:
                ticket.description = data["description"]

            ticket.save()
            return DataJsonResponse({"message": "Ticket updated successfully"})

        except Ticket.DoesNotExist:
            return ErrorJsonResponse("Ticket not found", status=404)
        except Exception as e:
            return ErrorJsonResponse(str(e), status=500)
        
    @action(detail=True, methods=["delete"])
    def delete(self, request, ticket_id=None):
        """
        Delete a ticket by ID.
        """
        try:
            ticket = Ticket.objects.get(pk=ticket_id)
            ticket.delete()
            return DataJsonResponse({"message": "Ticket deleted successfully"})

        except Ticket.DoesNotExist:
            return ErrorJsonResponse("Ticket not found", status=404)