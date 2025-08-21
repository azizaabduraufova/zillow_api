from django.db import models
from django.contrib.auth.models import User

class PropertyType(models.Model):
    type = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.type

class Property(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)

    property_type = models.ManyToManyField(PropertyType, related_name='properties')

    bedrooms = models.IntegerField(default=0)
    bathrooms = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    square_feet = models.IntegerField(null=True, blank=True)

    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)

    listed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)