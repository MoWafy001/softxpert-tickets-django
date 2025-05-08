from django.db import models
from .enums import Role

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=50, choices=[
        (Role.ADMIN, "Admin"), 
        (Role.SUPPORT_AGENT, 'Support Agent'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
