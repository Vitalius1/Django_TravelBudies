from __future__ import unicode_literals

from django.db import models
from ..log_reg.models import User
from datetime import datetime, timedelta, date

class BuddyManager(models.Manager):
    def create_plan(self, creator, trip):
        self.create(traveler = creator, trip = trip)
    
    # def not_joined(self, user_id):


class TripManager(models.Manager):
    def create_trip(self, postData):
        now = datetime.today().date()
        errors = {}
        print now, '********%%%$##$@#@#$@#@#@@#$%#'
        if not postData['destination'] or not postData['description'] or not postData['start_date'] or not postData['end_date']:
            errors['empty_error'] = "Fields can not be empty."
            print errors
        if len(errors):
            return (False, errors)

        start = datetime.strptime(str(postData['start_date']), "%Y-%m-%d").date()
        end = datetime.strptime(str(postData['end_date']), "%Y-%m-%d").date()
        print end

        if start < now:
            errors['start_error'] = "You can not choose your 'Date From' anything earlier than current date!"
        if end < start:
            errors['end_error'] = "You can not choose 'Date To' anything earlier than 'Date From'!"
        if len(errors):
            return (False, errors)
        else:
            creator = User.objects.get(id = postData['user_id'])
            trip = self.create(name = postData['destination'], description = postData['description'], creator = creator, start_date = start, end_date = end)
            Buddy.objects.create_plan(creator, trip)
            print Buddy.objects.all()
            return (True, "Succes")




class Trip(models.Model):
    name = models.CharField(max_length = 128)
    description = models.CharField(max_length = 128)
    creator = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "trips")
    start_date = models.DateTimeField(null = True)
    end_date = models.DateTimeField(null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = TripManager()

class Buddy(models.Model):
    traveler = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "buddies")
    trip = models.ForeignKey(Trip, on_delete = models.CASCADE, related_name = "trips")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = BuddyManager()



# Create your models here.
