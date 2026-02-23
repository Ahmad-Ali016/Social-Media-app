from django.db import models
from django.conf import settings    # to reference custom User mode

# Create your models here.

class Profile(models.Model):
    # One profile per user
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,   # custom user model
        on_delete=models.CASCADE,
        related_name='profile'      # allows user.profile access
    )

    bio = models.TextField(blank=True, null=True)

    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )

    location = models.CharField(max_length=100, blank=True, null=True)

    date_of_birth = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

