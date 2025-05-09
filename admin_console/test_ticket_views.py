from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from customers.models import Customer
from users.models import Admin
from django.utils import timezone
from tickets.models import Ticket
from users.models import Admin

class TicketViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = Admin.objects.create_user(
            username="admin", password="admint123"
        )
        self.client.force_authenticate(user=self.admin_user)
        self.valid_payload = {
            "title": "Test Ticket",
            "description": "This is a test ticket description.",
        }
        self.invalid_payload = {
            "title": "",
            "description": "",
        }

    def tearDown(self):
        self.client.logout()
        Ticket.objects.filter(title=self.valid_payload["title"]).delete()  # Clean up test data

    def test_create_ticket_success(self):
        """
        Ensure we can create a new ticket with valid payload.
        """
        response = self.client.post(
            reverse("admin-console:tickets"), self.valid_payload, format="json"
        )
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data["message"], "Ticket created successfully")
        self.assertTrue(Ticket.objects.filter(title=self.valid_payload["title"]).exists())

    def test_create_ticket_missing_fields(self):
        """
        Ensure we cannot create a ticket with missing fields.
        """
        response = self.client.post(
            reverse("admin-console:tickets"), self.invalid_payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title and description are required", response.json()["error"])

    def test_listing_tickets(self):
        """
        Ensure we can list all tickets.
        """
        Ticket.objects.create(
            title=f"Ticket {timezone.now().timestamp()}",
            description="Test ticket description.",
            created_by=self.admin_user,
        )
        response = self.client.get(reverse("admin-console:tickets"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data['data'], list)
        self.assertGreater(len(data['data']), 0)
        self.assertIn("id", data["data"][0])
        self.assertIn("title", data["data"][0])
        self.assertIn("description", data["data"][0])
        self.assertIn("created_at", data["data"][0])
        self.assertIn("updated_at", data["data"][0])

    def test_get_by_id_success(self):
        """
        Ensure we can retrieve a ticket by ID.
        """
        ticket = Ticket.objects.create(
            title=f"Ticket {timezone.now().timestamp()}",
            description="Test ticket description.",
            created_by=self.admin_user,
        )
        response = self.client.get(reverse("admin-console:ticket-by-id", args=[ticket.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()['data']
        self.assertEqual(data["id"], ticket.id)
        self.assertEqual(data["title"], ticket.title)
        self.assertEqual(data["description"], ticket.description)
        self.assertIn("created_at", data)
        self.assertIn("updated_at", data)

    def test_get_by_id_not_found(self):
        """
        Ensure we get a 404 error when trying to retrieve a non-existent ticket.
        """
        response = self.client.get(reverse("admin-console:ticket-by-id", args=[99999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Ticket not found", response.json()["error"])

    def test_update_by_id_success(self):
        """
        Ensure we can update a ticket by ID.
        """
        ticket = Ticket.objects.create(
            title=f"Ticket {timezone.now().timestamp()}",
            description="Test ticket description.",
            created_by=self.admin_user,
        )
        update_payload = {
            "title": "Updated Title",
            "description": "Updated description.",
        }
        response = self.client.patch(
            reverse("admin-console:ticket-by-id", args=[ticket.id]),
            update_payload,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["message"], "Ticket updated successfully")
        ticket.refresh_from_db()
        self.assertEqual(ticket.title, update_payload["title"])
        self.assertEqual(ticket.description, update_payload["description"])

    def test_delete_by_id_success(self):
        """
        Ensure we can delete a ticket by ID.
        """
        ticket = Ticket.objects.create(
            title=f"Ticket {timezone.now().timestamp()}",
            description="Test ticket description.",
            created_by=self.admin_user,
        )
        response = self.client.delete(reverse("admin-console:ticket-by-id", args=[ticket.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["message"], "Ticket deleted successfully")
        self.assertFalse(Ticket.objects.filter(id=ticket.id).exists())