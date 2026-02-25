# backend/products/models.py
import uuid
from django.db import models


class Category(models.Model):
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name        = models.CharField(max_length=100)
    slug        = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image_url   = models.TextField(blank=True)
    parent      = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    is_active   = models.BooleanField(default=True)
    sort_order  = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name


class Product(models.Model):
    class StockStatus(models.TextChoices):
        IN_STOCK  = 'in_stock', 'In Stock'
        OUT_STOCK = 'out_of_stock', 'Out of Stock'
        LOW_STOCK = 'low_stock', 'Low Stock'

    id                = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name              = models.CharField(max_length=255)
    slug              = models.SlugField(unique=True)
    description       = models.TextField(blank=True)
    short_description = models.CharField(max_length=500, blank=True)
    category          = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    price             = models.DecimalField(max_digits=10, decimal_places=2)
    compare_price     = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cost_price        = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sku               = models.CharField(max_length=100, unique=True)
    stock_quantity    = models.IntegerField(default=0)
    stock_status      = models.CharField(max_length=20, choices=StockStatus.choices, default=StockStatus.IN_STOCK)
    images            = models.JSONField(default=list)   # [{url, alt, is_primary}]
    attributes        = models.JSONField(default=dict)   # {color: red, size: M}
    weight            = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    is_active         = models.BooleanField(default=True)
    is_featured       = models.BooleanField(default=False)
    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name