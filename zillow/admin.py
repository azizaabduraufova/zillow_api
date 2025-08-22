from django.contrib import admin

from zillow.models import PropertyType, Property, Profile, ProfileType

# Register your models here.

admin.site.register([PropertyType,Property, Profile, ProfileType])

