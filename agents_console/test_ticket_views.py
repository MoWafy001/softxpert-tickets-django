from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from customers.models import Customer
from django.utils import timezone
from tickets.models import Ticket
from users.models import SupportAgent, Admin

class TicketViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.agent_user = SupportAgent.objects.create_user(
            username="agent", password="agent123"
        )
        self.admin_user = Admin.objects.create_user(
            username="admin", password="admin123"
        )
        self.client.force_authenticate(user=self.agent_user)
        self.valid_payload = {
            "title": "Test Ticket",
            "description": "This is a test ticket description.",
        }
        self.invalid_payload = {
            "title": "",
            "description": "",
        }

    def test_listing_tickets(self):
        """
        Ensure we can list all tickets.
        """
        Ticket.objects.create(
            title=f"Ticket {timezone.now().timestamp()}",
            description="Test ticket description.",
            created_by=self.admin_user,
        )
        response = self.client.get(reverse("agents-console:tickets"))
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
            assigned_to=self.agent_user,
        )
        response = self.client.get(reverse("agents-console:ticket-by-id", args=[ticket.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()['data']
        self.assertEqual(data["id"], ticket.id)
        self.assertEqual(data["title"], ticket.title)
        self.assertEqual(data["description"], ticket.description)
        self.assertIn("created_at", data)
        self.assertIn("updated_at", data)

    def test_should_auto_assign_15_tickets_on_fetch(self):
        """
        Ensure that when an agent fetches tickets, they are automatically assigned 15 tickets.
        """
        # clear any existing tickets
        Ticket.objects.all().delete()

        # Create 20 unassigned tickets
        for i in range(20):
            Ticket.objects.create(
                title=f"Ticket {i}",
                description="Test ticket description.",
                created_by=self.admin_user,
            )

        # user should have 0 tickets assigned
        no_tickets_assigned_to_agent = Ticket.objects.filter(assigned_to=self.agent_user).count()
        self.assertEqual(no_tickets_assigned_to_agent, 0)

        # Fetch tickets
        response = self.client.get(reverse("agents-console:tickets"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data['data'], list)
        self.assertEqual(len(data['data']), 15)
        self.assertIn("id", data["data"][0])
        self.assertIn("title", data["data"][0])
        self.assertIn("description", data["data"][0])
        self.assertIn("created_at", data["data"][0])
        self.assertIn("updated_at", data["data"][0])


    def test_get_by_id_not_found(self):
        """
        Ensure we get a 404 error when trying to retrieve a non-existent ticket.
        """
        response = self.client.get(reverse("agents-console:ticket-by-id", args=[99999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Ticket not found", response.json()["error"])