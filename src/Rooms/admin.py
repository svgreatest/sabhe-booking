from django.contrib import admin
from .models import Rooms
from .models import Booking

from django.contrib.admin import AdminSite

class MyAdminSite(AdminSite):
    site_header = "Vaidhika Dharma Sahaaya Sabha Room Booking System"

# Register your models here.
admin_site = MyAdminSite(name='sabhe-booking')
admin_site.register(Rooms)
admin_site.register(Booking)
