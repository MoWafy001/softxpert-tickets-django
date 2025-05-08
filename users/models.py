from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .enums import Role

class UserManager(models.Manager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)

class User(AbstractBaseUser):
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

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'role']
    objects = UserManager()

    def __str__(self):
        return self.username
    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, name={self.name}, role={self.role})"

    class Meta:
        db_table = 'users'
