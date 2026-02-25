# backend/reviews/models.py
import uuid
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    id                   = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user                 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product              = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='reviews')
    order                = models.ForeignKey('orders.Order', on_delete=models.SET_NULL, null=True, blank=True)
    rating               = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title                = models.CharField(max_length=255, blank=True)
    body                 = models.TextField(blank=True)
    images               = models.JSONField(default=list)
    is_verified_purchase = models.BooleanField(default=False)
    is_approved          = models.BooleanField(default=False)
    helpful_count        = models.IntegerField(default=0)
    created_at           = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} → {self.product.name} ({self.rating}★)"