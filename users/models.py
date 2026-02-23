from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    # Email as unique identifier for login
    email = models.EmailField(unique=True)

    # Profile picture for each user
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    # Short biography
    bio = models.TextField(max_length=500, blank=True)

    # Date of birth
    date_of_birth = models.DateField(null=True, blank=True)

    # Gender options
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)

    # Account privacy
    is_private_account = models.BooleanField(default=False)

    # User creation timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    # Use email as login field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Username still required for superuser

    def __str__(self):
        return self.email