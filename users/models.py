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

class UserRoleManager(models.Manager):
    def __init__(self, role: Role):
        super().__init__()
        self.role = role

    def get_queryset(self):
        return super().get_queryset().filter(role=self.role)

class Admin(User):
    class Meta:
        proxy = True

    objects = UserRoleManager(Role.ADMIN)
    def __str__(self):
        return f"Admin: {self.username}"
    def __repr__(self):
        return f"Admin(id={self.id}, username={self.username}, name={self.name})"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role = Role.ADMIN
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.role = Role.ADMIN
        return instance

class SupportAgent(User):
    class Meta:
        proxy = True

    objects = UserRoleManager(Role.SUPPORT_AGENT)
    def __str__(self):
        return f"SupportAgent: {self.username}"
    def __repr__(self):
        return f"SupportAgent(id={self.id}, username={self.username}, name={self.name})"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role = Role.SUPPORT_AGENT
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.role = Role.SUPPORT_AGENT
        return instance