from __future__ import unicode_literals
from django.db import models
from datetime import datetime, date
import re

class UserManager(models.Manager):
    def create_validator(self, reqPOST):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(reqPOST['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters."

        if len(reqPOST['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters."

        email_taken = User.objects.filter(email=reqPOST['email'])
        if len(email_taken) > 0:
            errors['email_taken'] = "Email already in use."

        if not EMAIL_REGEX.match(reqPOST['email']):
            errors['regex'] = "Email is not in correct format."

        if reqPOST['birthday'] == '':
            errors['birthday'] = "Must enter a birthday."

        else:
            today = datetime.today()
            birthday = datetime.strptime(reqPOST['birthday'], '%Y-%m-%d')
            if today.year - birthday.year < 13:
                errors['birthdate_requirement'] = "You are not old enough to use this application."

            if datetime.strptime(reqPOST['birthday'], '%Y-%m-%d') > datetime.today():
                errors['birthday_past'] = "Birthdate must be in the past."

        if len(reqPOST['password']) < 8:
            errors['password'] = "Password must be at least 8 characters."

        if reqPOST['password'] != reqPOST['pw_confirm']:
            errors['password_match'] = "Password and password confirmation must match."

        return errors

class TripManager(models.Manager):
    def create_validator(self, reqPOST):
        errors = {}

        if reqPOST['destination'] == '':
            errors['destination'] = "Must enter a destination."

        if reqPOST['plan'] == '':
            errors['plan'] = "Must enter a trip plan."

        if reqPOST['date_from'] == '' or reqPOST['date_to'] == '':
            errors['no_date'] = "Must enter both dates."

        else:
            if datetime.strptime(reqPOST['date_to'], '%Y-%m-%d') < datetime.strptime(reqPOST['date_from'], '%Y-%m-%d'):
                errors['to_before_from'] = "Travel end date must be after start date."

            if datetime.strptime(reqPOST['date_from'], '%Y-%m-%d') < datetime.today() or datetime.strptime(reqPOST['date_to'], '%Y-%m-%d') < datetime.today():
                errors['from_not_in_future'] = "Travel dates must be in the future."

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    birthday = models.DateField()
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    destination = models.TextField()
    plan = models.TextField()
    date_from = models.DateField()
    date_to = models.DateField()
    creator = models.ForeignKey(User, related_name="created_trips", on_delete=models.CASCADE)
    attendees = models.ManyToManyField(User, related_name="trips_attending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()