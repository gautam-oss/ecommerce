# backend/orders/models.py
import uuid
from django.db import models
from django.conf import settings


class Coupon(models.Model):
    class DiscountType(models.TextChoices):
        PERCENTAGE = 'percentage', 'Percentage'
        FIXED      = 'fixed', 'Fixed Amount'

    id                  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code                = models.CharField(max_length=50, unique=True)
    description         = models.TextField(blank=True)
    discount_type       = models.CharField(max_length=15, choices=DiscountType.choices)
    discount_value      = models.DecimalField(max_digits=10, decimal_places=2)
    min_order_amount    = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    usage_limit         = models.IntegerField(null=True, blank=True)
    used_count          = models.IntegerField(default=0)
    is_active           = models.BooleanField(default=True)
    valid_from          = models.DateTimeField()
    valid_until         = models.DateTimeField()

    def __str__(self):
        return self.code


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING   = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        SHIPPED   = 'shipped', 'Shipped'
        DELIVERED = 'delivered', 'Delivered'
        CANCELLED = 'cancelled', 'Cancelled'
        REFUNDED  = 'refunded', 'Refunded'

    id                  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number        = models.CharField(max_length=20, unique=True)
    user                = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='orders')
    shipping_address    = models.ForeignKey('users.Address', on_delete=models.PROTECT, null=True)
    coupon              = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    status              = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING)
    subtotal            = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount     = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_cost       = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount          = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount        = models.DecimalField(max_digits=10, decimal_places=2)
    notes               = models.TextField(blank=True)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.order_number

    def save(self, *args, **kwargs):
        if not self.order_number:
            import random, string
            self.order_number = 'ORD-' + ''.join(random.choices(string.digits, k=8))
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    id             = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order          = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product        = models.ForeignKey('products.Product', on_delete=models.PROTECT)
    product_name   = models.CharField(max_length=255)   # snapshot
    product_sku    = models.CharField(max_length=100)   # snapshot
    quantity       = models.PositiveIntegerField()
    unit_price     = models.DecimalField(max_digits=10, decimal_places=2)
    total_price    = models.DecimalField(max_digits=10, decimal_places=2)
    attributes     = models.JSONField(default=dict)     # snapshot

    def __str__(self):
        return f"{self.product_name} x{self.quantity}"