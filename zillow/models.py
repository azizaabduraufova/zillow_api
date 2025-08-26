from datetime import timezone

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

    property_type = models.ManyToManyField(PropertyType, related_name='properties', default="House")

    bedrooms = models.IntegerField(default=0)
    bathrooms = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    square_feet = models.IntegerField(null=True, blank=True)

    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)

    listed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ProfileType(models.Model):
    type = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.type

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    profile_type = models.ManyToManyField(ProfileType, related_name='profiles', default="Buyer")
    phone = models.CharField(max_length=15, unique=True)
    img = models.ImageField(null=True, blank=True, upload_to='profile_pics/')

    def __str__(self):
        return f"{self.user.username}: {self.phone}"

class WatchedHistory(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='watched_history')
    property=models.ForeignKey(Property,on_delete=models.CASCADE,related_name='watched_history')
    watched_at=models.DateTimeField(auto_now_add=True)
    is_deleted=models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user.username} : {self.property.title} :{self.watched_at.strftime('')}"


