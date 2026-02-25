# backend/payments/models.py
import uuid
from django.db import models
from django.conf import settings


class Payment(models.Model):
    class Method(models.TextChoices):
        CARD       = 'card', 'Card'
        UPI        = 'upi', 'UPI'
        WALLET     = 'wallet', 'Wallet'
        COD        = 'cod', 'Cash on Delivery'
        NETBANKING = 'netbanking', 'Net Banking'

    class Status(models.TextChoices):
        PENDING  = 'pending', 'Pending'
        SUCCESS  = 'success', 'Success'
        FAILED   = 'failed', 'Failed'
        REFUNDED = 'refunded', 'Refunded'

    id               = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order            = models.OneToOneField('orders.Order', on_delete=models.PROTECT, related_name='payment')
    user             = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    amount           = models.DecimalField(max_digits=10, decimal_places=2)
    currency         = models.CharField(max_length=3, default='INR')
    method           = models.CharField(max_length=15, choices=Method.choices)
    status           = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    gateway          = models.CharField(max_length=50, blank=True)   # stripe / razorpay
    gateway_txn_id   = models.CharField(max_length=255, blank=True)
    gateway_response = models.JSONField(default=dict)
    paid_at          = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Payment {self.id} - {self.status}"