from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    roles = (
        ('USER', 'Regular User'), 
        ('MANAGER', 'User Manager'), 
        ('ADMIN', 'Administrator')
    )
    role = models.CharField(choices=roles, default=roles[0][0], max_length=20)
    userId = models.OneToOneField(User, on_delete=models.CASCADE)