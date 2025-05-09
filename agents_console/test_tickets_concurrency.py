from django.test import LiveServerTestCase
from django.urls import reverse
from rest_framework.test import APIClient
from tickets.models import Ticket
from users.models import SupportAgent, Admin
from threading import Thread
from django.db import connection

class TicketConcurrencyTests(LiveServerTestCase):
    def setUp(self):
        self.creator_admin = Admin.objects.create_user(
            username="admin", password="admin123"
        )

        # Create 30 unassigned tickets
        for i in range(60):
            Ticket.objects.create(title=f"Ticket {i}", description="Test ticket", created_by=self.creator_admin)

        # Create 3 agent users
        self.agents = []
        for i in range(4):
            agent = SupportAgent.objects.create_user(username=f"agent{i}", password="password")
            self.agents.append(agent)

    def test_concurrent_ticket_assignment(self):
        """
        Test that tickets are assigned correctly under concurrent access.
        """
        def assign_tickets(agent):
            client = APIClient()
            client.force_authenticate(user=agent)
            response = client.get(f"{self.live_server_url}{reverse('agents-console:tickets')}")
            self.assertEqual(response.status_code, 200)
            connection.close()

        # Create threads for each agent
        threads = []
        for agent in self.agents:
            thread = Thread(target=assign_tickets, args=(agent,))
            threads.append(thread)

        # Start all threads
        for thread in threads:
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        # Verify that no tickets are assigned to multiple agents
        assigned_tickets = Ticket.objects.exclude(assigned_to=None)
        assigned_ticket_ids = [ticket.id for ticket in assigned_tickets]
        self.assertEqual(len(assigned_ticket_ids), len(set(assigned_ticket_ids)))

        # Verify that each agent has at most 15 tickets
        for agent in self.agents:
            agent_ticket_count = Ticket.objects.filter(assigned_to=agent).count()
            self.assertLessEqual(agent_ticket_count, 15)

        # Verify that all tickets are assigned
        total_assigned_tickets = Ticket.objects.exclude(assigned_to=None).count()
        self.assertEqual(total_assigned_tickets, 60)