from django.contrib import admin
from .models import Cargo, Location, Car

# Register your models here.
admin.site.register(Cargo)
admin.site.register(Location)
admin.site.register(Car)