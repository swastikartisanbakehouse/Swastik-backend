from django.db import models
from apps.categories.models import Category

class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    subcategory_name = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField(blank=True, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    unit = models.CharField(max_length=50, default='1 Pc')
    stock_quantity = models.IntegerField(default=100)
    is_available = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, default='Swastik')
    tags = models.JSONField(default=list, blank=True)
    attributes = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)



    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.sku}] {self.name} - ₹{self.price} ({self.unit})"
