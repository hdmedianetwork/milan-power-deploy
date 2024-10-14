from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

ROLE_CHOICE = (
    ('salesman', 'Salesman'),
    ('receiver', 'Receiver'),
    ('checker', 'Checker'),
    ('accountant', 'Accountant'),
    ('admin', 'Admin'),
) 

class User(AbstractUser):
    email = models.EmailField(unique=True, null=False)
    username = models.CharField(max_length=200, name=False)
    role = models.CharField(choices=ROLE_CHOICE, max_length=30)

    USERNAME_FIELD = "email" # Changes the initial username field to email
    REQUIRED_FIELDS = ['username']

    
