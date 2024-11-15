from django.contrib.auth.models import User
from django.db import models

# Extending the User model with a one-to-one relationship to store additional user information.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dietary_preferences = models.TextField(blank=True)
    allergies = models.TextField(blank=True)