from django.db import models
from mainapp import admin
# Create your models here.

class Admin(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=256)
    status = models.CharField(max_length=10, default='active')
