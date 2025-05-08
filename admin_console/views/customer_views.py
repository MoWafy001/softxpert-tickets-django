from common.json_responses import DataJsonResponse, ErrorJsonResponse
from customers.models import Customer
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from common.csrf_except_ession_authentication import CsrfExemptSessionAuthentication


class CustomerViewSet(APIView):
    """
    ViewSet for managing customers.
    """

    authentication_classes = (CsrfExemptSessionAuthentication, SessionAuthentication)
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"])
    def post(self, request):
        """
        Create a new customer.
        """
        if request.method != "POST":
            return DataJsonResponse("Invalid request method", status=405)

        try:
            data = request.data
            name = data.get("name")
            email = data.get("email")

            if not name or not email:
                return DataJsonResponse({"error": "name and email are required"}, status=400)

            customer = Customer.objects.create(name=name, email=email)
            return DataJsonResponse({"message": "Customer created successfully", "customer_id": customer.id}, status=201)

        except Exception as e:
            return ErrorJsonResponse(str(e), status=500)
        
    
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
            }
            for customer in customers
        ]
        return DataJsonResponse(customers_list)

class CustomerByIdViewSet(APIView):
    """
    ViewSet for managing customers by ID.
    """

    authentication_classes = (CsrfExemptSessionAuthentication, SessionAuthentication)
    permission_classes = [IsAuthenticated]

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
            }
            return DataJsonResponse(customer_data)

        except Customer.DoesNotExist:
            return ErrorJsonResponse("Customer not found", status=404)
        except Exception as e:
            return ErrorJsonResponse(str(e), status=500)

    @action(detail=True, methods=["patch"])
    def patch(self, request, customer_id=None):
        """
        Update a customer by ID.
        """
        try:
            customer = Customer.objects.get(pk=customer_id)
            data = request.data

            if "name" in data:
                customer.name = data["name"]
            if "email" in data:
                customer.email = data["email"]

            customer.save()
            return DataJsonResponse({"message": "Customer updated successfully"})

        except Customer.DoesNotExist:
            return ErrorJsonResponse("Customer not found", status=404)
        except Exception as e:
            return ErrorJsonResponse(str(e), status=500)
        
    @action(detail=True, methods=["delete"])
    def delete(self, request, customer_id=None):
        """
        Delete a customer by ID.
        """
        try:
            customer = Customer.objects.get(pk=customer_id)
            customer.delete()
            return DataJsonResponse({"message": "Customer deleted successfully"})

        except Customer.DoesNotExist:
            return ErrorJsonResponse("Customer not found", status=404)