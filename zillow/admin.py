from django.contrib import admin

from zillow.models import PropertyType,Property

# Register your models here.

admin.site.register([PropertyType,Property])

