# backend/users/models.py
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        CUSTOMER = 'customer', 'Customer'
        ADMIN    = 'admin', 'Admin'
        STAFF    = 'staff', 'Staff'

    id         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email      = models.EmailField(unique=True)
    username   = models.CharField(max_length=50, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name  = models.CharField(max_length=50, blank=True)
    phone      = models.CharField(max_length=20, blank=True)
    role       = models.CharField(max_length=10, choices=Role.choices, default=Role.CUSTOMER)
    avatar_url = models.TextField(blank=True)
    is_active  = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_staff   = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Address(models.Model):
    class AddressType(models.TextChoices):
        SHIPPING = 'shipping', 'Shipping'
        BILLING  = 'billing', 'Billing'

    id            = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user          = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    full_name     = models.CharField(max_length=100)
    phone         = models.CharField(max_length=20, blank=True)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city          = models.CharField(max_length=100)
    state         = models.CharField(max_length=100)
    postal_code   = models.CharField(max_length=20)
    country       = models.CharField(max_length=100)
    is_default    = models.BooleanField(default=False)
    address_type  = models.CharField(max_length=10, choices=AddressType.choices, default=AddressType.SHIPPING)

    class Meta:
        verbose_name_plural = 'addresses'

    def __str__(self):
        return f"{self.full_name} - {self.city}"