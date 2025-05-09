from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from customers.models import Customer
from users.models import Admin
from django.utils import timezone

class CustomerViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = Admin.objects.create_user(
            username="admin", password="admin123"
        )
        self.client.force_authenticate(user=self.admin_user)
        self.valid_payload = {
            "name": "John Doe",
            "email": f"johndoe{timezone.now().timestamp()}@example.com",
        }
        self.invalid_payload = {
            "name": "",
            "email": "",
        }

    def tearDown(self):
        self.client.logout()
        Customer.objects.filter(
            email=self.valid_payload["email"]
        ).delete()  # Clean up test data

    def test_create_customer_success(self):
        """
        Ensure we can create a new customer with valid payload.
        """
        response = self.client.post(
            reverse("admin-console:customers"), self.valid_payload, format="json"
        )
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data["message"], "Customer created successfully")
        self.assertTrue(Customer.objects.filter(email=self.valid_payload["email"]).exists())

    def test_create_customer_missing_fields(self):
        """
        Ensure we cannot create a customer with missing fields.
        """
        response = self.client.post(
            reverse("admin-console:customers"), self.invalid_payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name and email are required", response.json()["error"])

    def test_listing_customers(self):
        """
        Ensure we can list all customers.
        """
        Customer.objects.create(
            name=f"Customer {timezone.now().timestamp()}",
            email=f"testEmail{timezone.now().timestamp()}@example.com",
        )
        response = self.client.get(reverse("admin-console:customers"))
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
        response = self.client.get(reverse("admin-console:customer-by-id", args=[customer.id]))
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
        response = self.client.get(reverse("admin-console:customer-by-id", args=[99999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Customer not found", response.json()["error"])

    def test_update_by_id_success(self):
        """
        Ensure we can update a customer by ID.
        """
        customer = Customer.objects.create(
            name=f"Customer {timezone.now().timestamp()}",
            email=f"testEmail{timezone.now().timestamp()}@example.com",
        )
        update_payload = {
            "name": "Updated Name",
            "email":f"updatedTestEmail{timezone.now().timestamp()}@example.com",
        }
        response = self.client.patch(
            reverse("admin-console:customer-by-id", args=[customer.id]),
            update_payload,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["message"], "Customer updated successfully")
        customer.refresh_from_db()
        self.assertEqual(customer.name, update_payload["name"])
        self.assertEqual(customer.email, update_payload["email"])

    def test_delete_by_id_success(self):
        """
        Ensure we can delete a customer by ID.
        """
        customer = Customer.objects.create(
            name=f"Customer {timezone.now().timestamp()}",
            email=f"testEmail{timezone.now().timestamp()}@example.com",
        )
        response = self.client.delete(reverse("admin-console:customer-by-id", args=[customer.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["message"], "Customer deleted successfully")
        self.assertFalse(Customer.objects.filter(id=customer.id).exists())