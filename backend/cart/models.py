# backend/cart/models.py
import uuid
from django.db import models
from django.conf import settings


class CartItem(models.Model):
    id                   = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user                 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart_items')
    product              = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity             = models.PositiveIntegerField(default=1)
    selected_attributes  = models.JSONField(default=dict)
    added_at             = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.email} → {self.product.name}"