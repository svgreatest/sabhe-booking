from django.db import models
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
import datetime
from . import utils

# Create your models here.
class Rooms(models.Model):
    ROOM_TYPES = (
        ('SB', 'Shraddha Bhavana'),
        ('Cottage', 'Cottage'),
        ('Mantap', 'Mantap'),
        ('APB', 'Annapurneshwari Bhavan'),
    )
    room_id = models.CharField(max_length=100, unique=True)
    room_type = models.CharField(max_length=100, choices=ROOM_TYPES)
    price = models.IntegerField()

    def __str__(self):
        return '{} {} {}'.format(self.room_id, self.room_type, self.price)

    def get_absolute_url(self):
        return reverse('Rooms:room_edit', kwargs={'pk': self.pk})

    def get_room_types():
        return ROOM_TYPES

class Booking(models.Model):
    BOOKING_STATUS_CHOICES = (
        ('Booked', 'Booked'),
        ('Cancelled', 'Cancelled'),
    )
    name = models.CharField(max_length=200, default="")
    caste = models.CharField(max_length=200, default="")
    subcaste = models.CharField(max_length=200, default="" )
    gothra = models.CharField(max_length=200, default="")
    nakshatra = models.CharField(max_length=200, default="")
    contact = models.CharField(max_length=10,default="")
    email = models.EmailField(max_length=254)
    room = models.CharField(max_length=254,default="")
    start = models.DateField()
    end = models.DateField()
    booked_on = models.DateField(auto_now_add=True, )
    status = models.CharField(max_length=100, default="Booked",
                              choices=BOOKING_STATUS_CHOICES)

    def __str__(self):
        return '%s %s' % (self.name, str(self.contact))

class Donations(models.Model):
    DONATION_CHOICES = (
        ('Puduvattu', 'Puduvattu'),
        ('Annadaana nidhi', 'Annadaana nidhi'),
        ('BLD', 'Building fund'),
        ('OTH', 'Others'),
        ('Aparakarma nidhi', 'Aparakarma nidhi'),
    )
    name = models.CharField(max_length=200)
    caste = models.CharField(max_length=200)
    subcaste = models.CharField(max_length=200)
    gothra = models.CharField(max_length=200)
    nakshatra = models.CharField(max_length=200)
    contact = models.CharField(max_length=10)
    email = models.EmailField(max_length=254)
    reason = models.CharField(max_length = 254, choices=DONATION_CHOICES)
    date = models.DateField(auto_now=True)
    amount = models.CharField(max_length = 254, default="")
    booked_on = models.DateField(auto_now_add=True, )

class Ambulance(models.Model):
    AMBULANCE_CHOICES = (
        ('Van', 'VAN'),
        ('OBSM', 'Obs. materials'),
        ('OTH', 'Others'),
    )
    name = models.CharField(max_length=200)
    caste = models.CharField(max_length=200)
    subcaste = models.CharField(max_length=200)
    gothra = models.CharField(max_length=200)
    nakshatra = models.CharField(max_length=200)
    contact = models.CharField(max_length=10)
    email = models.EmailField(max_length=254)
    reason = models.CharField(max_length = 254, choices=AMBULANCE_CHOICES)
    date = models.DateField(auto_now=True)
    amount = models.CharField(max_length = 254, default="")
    booked_on = models.DateField(auto_now_add=True, )

class Expenses(models.Model):
    EXPENSE_CATEGORIES = (
        ('Obs. materials', 'Obs. materials'),
        ('Others', 'Others'),
    )
    category = models.CharField(max_length=200, choices=EXPENSE_CATEGORIES)
    sub_category = models.CharField(max_length=500)
    to = models.CharField(max_length=1000)
    amount = models.CharField(max_length=500)
    mode_of_payment = models.CharField(max_length=1000, default="Cash")
    booked_on = models.DateField(auto_now_add=True, )
