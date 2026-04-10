from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
# Create your models here.

class User(AbstractUser):
    #Abstract User already give fields like username password first name last name  so we donot declare it here
    phone_regex = RegexValidator(
        regex=r'^\d{10,15}$', 
        message="Phone number must be between 10 to 15 digits. Only numbers allowed."
    )

    phone = models.CharField(
        validators=[phone_regex], 
        max_length=15, 
        unique=True
    )
    role = models.CharField(max_length=10)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
    

# USERNAME_FIELD = 'username'