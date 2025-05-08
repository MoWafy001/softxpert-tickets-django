from django.db import models

class CustomerManager(models.Manager):
    def create_customer(self, name, email):
        customer = self.create(name=name, email=email)
        return customer

    def get_customers(self):
        return self.all()

    def get_customer_by_id(self, customer_id):
        return self.get(id=customer_id)

    def update_customer(self, customer_id, name=None, email=None):
        customer = self.get(id=customer_id)
        if name:
            customer.name = name
        if email:
            customer.email = email
        customer.save()
        return customer

    def delete_customer(self, customer_id):
        customer = self.get(id=customer_id)
        customer.delete()

# Create your models here.
class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects: CustomerManager = CustomerManager()

    class Meta:
        db_table = "customers"

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Customer(id={self.id}, name={self.name}, email={self.email})"