from django.db import models

# Create your models here.
class Ticket(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    assigned_to = models.ForeignKey(
        'users.SupportAgent',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tickets_assigned'
    )
    created_by = models.ForeignKey(
        'users.Admin',
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='tickets_created'
    )
    sold_to = models.ForeignKey(
        'customers.Customer',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tickets_sold'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tickets'
        ordering = ['-created_at']

    def __str__(self):
        return self.title