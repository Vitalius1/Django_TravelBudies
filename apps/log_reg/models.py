from __future__ import unicode_literals

from django.db import models
import bcrypt


class UserManager(models.Manager):
    def validate_and_register(self, postData):
        errors = {}
        
        # First Name Validation
        if not len(postData['name']):
            errors['name'] = "Name field can not be empty."
        elif len(postData['name']) < 3:
            errors['name'] = "Name too short."
        
        # Username Validation
        if not len(postData['username']):
            errors['username'] = "Username field can not be empty."
        elif len(postData['username']) < 3:
            errors['username'] = "Username too short."
        elif self.filter(username = postData['username']):
            errors['username'] = "Error! Username already in use."
        
        
        # Password Validation
        if not len(postData['password']):
            errors['password'] = "Password field can not be empty."
        elif len(postData['password']) < 8:
            errors['password'] = "Password too short. Input at least 8 characters"
        elif postData['password'] != postData['confirm_pass']:
            errors['confirm_pass'] = "Password not confirmed. Please pay more attention"
       
        # Return of the validation results for register method
        if len(errors):
            return (False, errors)
        else:
            password = postData['password'].encode()
            hashed = bcrypt.hashpw(password, bcrypt.gensalt())
            self.create(name = postData['name'], username = postData['username'], password = hashed)
            return (True, postData['name'])

    def validate_and_login(self, postData):
        errors_login = {}
        # Username Validation when Login
        if not len(postData['username']):
            errors_login['login_username_error'] = "Please provide an username."
        else:
            if not self.filter(username = postData['username']):
                errors_login['login_error'] = "Username or password wrong."
        
        if not len(errors_login):
            user = self.filter(username = postData['username'])
        # # Password Validation when Login
            if not len(postData['password']):
                errors_login['login_password_error'] = "Please provide password."
            else:
                password = postData['password'].encode()
                hashed = self.filter(username = postData['username'])[0].password.encode()
                if not bcrypt.checkpw(password, hashed):
                    errors_login['login_error'] = "Username or password wrong."

        
        # Return of the validation results for login method
        if len(errors_login):
            return (False, errors_login)
        else:
            return (True, self.filter(username = postData['username']))





class User(models.Model):
    name = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
# Create your models here.
