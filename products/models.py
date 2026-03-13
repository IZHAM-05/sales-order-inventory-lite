from django.db import models
import uuid

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)

    sku = models.CharField(
        max_length=100,
        unique=True,
        blank=True
    )

    description = models.TextField(blank=True, null=True)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):

        if not self.sku:
            self.sku = "SKU-" + str(uuid.uuid4())[:8].upper()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.sku})"