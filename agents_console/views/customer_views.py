from common.json_responses import DataJsonResponse, ErrorJsonResponse
from customers.models import Customer
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from common.csrf_except_session_authentication import CsrfExemptSessionAuthentication
from users.permissions import IsAgent


class CustomerViewSet(APIView):
    """
    ViewSet for managing customers.
    """

    authentication_classes = (CsrfExemptSessionAuthentication, SessionAuthentication)
    permission_classes = [IsAuthenticated, IsAgent]

    @action(detail=False, methods=["get"])
    def get(self, request):
        """
        List all customers.
        """
        customers = Customer.objects.all()
        customers_list = [
            {
                "id": customer.id,
                "name": customer.name,
                "email": customer.email,
                "created_at": customer.created_at,
                "updated_at": customer.updated_at,
            }
            for customer in customers
        ]
        return DataJsonResponse(customers_list)

class CustomerByIdViewSet(APIView):
    """
    ViewSet for managing customers by ID.
    """

    authentication_classes = (CsrfExemptSessionAuthentication, SessionAuthentication)
    permission_classes = [IsAuthenticated, IsAgent]

    @action(detail=False, methods=["get"])
    def get(self, request, customer_id=None):
        """
        Retrieve a customer by ID.
        """
        try:
            customer = Customer.objects.get(pk=customer_id)
            customer_data = {
                "id": customer.id,
                "name": customer.name,
                "email": customer.email,
                "created_at": customer.created_at,
                "updated_at": customer.updated_at,
            }
            return DataJsonResponse(customer_data)

        except Customer.DoesNotExist:
            return ErrorJsonResponse("Customer not found", status=404)
        except Exception as e:
            return ErrorJsonResponse(str(e), status=500)