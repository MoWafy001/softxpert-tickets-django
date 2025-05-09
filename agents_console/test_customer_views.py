from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from customers.models import Customer
from users.models import SupportAgent
from django.utils import timezone

class CustomerViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.agent_user = SupportAgent.objects.create_user(
            username="agent", password="agent123"
        )
        self.client.force_authenticate(user=self.agent_user)

    def test_listing_customers(self):
        """
        Ensure we can list all customers.
        """
        Customer.objects.create(
            name=f"Customer {timezone.now().timestamp()}",
            email=f"testEmail{timezone.now().timestamp()}@example.com",
        )
        response = self.client.get(reverse("agents-console:customers"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data['data'], list)
        self.assertGreater(len(data['data']), 0)
        self.assertIn("id", data["data"][0])
        self.assertIn("name", data["data"][0])
        self.assertIn("email", data["data"][0])
        self.assertIn("created_at", data["data"][0])
        self.assertIn("updated_at", data["data"][0])

    def test_get_by_id_success(self):
        """
        Ensure we can retrieve a customer by ID.
        """
        customer = Customer.objects.create(
            name=f"Customer {timezone.now().timestamp()}",
            email=f"testEmail{timezone.now().timestamp()}@example.com",
        )
        response = self.client.get(reverse("agents-console:customer-by-id", args=[customer.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()['data']
        self.assertEqual(data["id"], customer.id)
        self.assertEqual(data["name"], customer.name)
        self.assertEqual(data["email"], customer.email)
        self.assertIn("created_at", data)
        self.assertIn("updated_at", data)

    def test_get_by_id_not_found(self):
        """
        Ensure we get a 404 error when trying to retrieve a non-existent customer.
        """
        response = self.client.get(reverse("agents-console:customer-by-id", args=[99999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Customer not found", response.json()["error"])