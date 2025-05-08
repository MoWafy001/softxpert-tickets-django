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

    def get_by_natural_key(self, username):
        return self.get(username=username)

class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=50, choices=[
        (Role.ADMIN.value, "Admin"), 
        (Role.SUPPORT_AGENT.value, 'Support Agent'),
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

class UserRoleManager(UserManager):
    def __init__(self, role: Role):
        super().__init__()
        self.role = role

    def create_user(self, username, password=None, **extra_fields):
        return super().create_user(username, password, **extra_fields, role=self.role)

    def get_queryset(self):
        return super().get_queryset().filter(role=self.role)

class Admin(User):
    class Meta:
        proxy = True

    objects = UserRoleManager(Role.ADMIN.value)
    def __str__(self):
        return f"Admin: {self.username}"
    def __repr__(self):
        return f"Admin(id={self.id}, username={self.username}, name={self.name})"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role = Role.ADMIN.value
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.role = Role.ADMIN.value
        return instance

class SupportAgent(User):
    class Meta:
        proxy = True

    objects = UserRoleManager(Role.SUPPORT_AGENT.value)
    def __str__(self):
        return f"SupportAgent: {self.username}"
    def __repr__(self):
        return f"SupportAgent(id={self.id}, username={self.username}, name={self.name})"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role = Role.SUPPORT_AGENT.value
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.role = Role.SUPPORT_AGENT.value
        return instance