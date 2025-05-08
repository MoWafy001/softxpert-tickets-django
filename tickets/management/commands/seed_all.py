from django.core.management.base import BaseCommand
from users.models import User, Admin, SupportAgent
from customers.models import Customer

class Command(BaseCommand):
    help = "Seed the database with mock data for all models"

    def handle(self, *args, **kwargs):
        # clear db
        User.objects.all().delete()
        Customer.objects.all().delete()

        # Seed 5 admins
        for _ in range(1,6):
            admin = Admin.objects.create_user(
                username=f"admin{_}",
                password="123",
                name=f"Admin {_}",
            )
            self.stdout.write(self.style.SUCCESS(f"Admin {admin.username} created."))
        self.stdout.write(self.style.SUCCESS("5 Admins created."))
        
        # Seed 5 support agents
        for _ in range(1,6):
            support_agent = SupportAgent.objects.create_user(
                username=f"support_agent{_}",
                password="123",
                name=f"Support Agent {_}",
            )
            self.stdout.write(self.style.SUCCESS(f"Support Agent {support_agent.username} created."))
        self.stdout.write(self.style.SUCCESS("5 Support Agents created."))

        # Seed 5 customers
        for _ in range(1,6):
            customer = Customer.objects.create_customer(
                name=f"Customer {_}",
                email=f"custtomer-{_}@app.com",
            )
            self.stdout.write(self.style.SUCCESS(f"Customer {customer.name} created."))
        self.stdout.write(self.style.SUCCESS("5 Customers created."))

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))