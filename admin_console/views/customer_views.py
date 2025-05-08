from common.data_json_response import DataJsonResponse
from customers.models import Customer


def list_customers_view(request):
    """
    View to list all customers.
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