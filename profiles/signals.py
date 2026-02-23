from django.conf import settings
from profiles.models import Profile
from django.dispatch import receiver
from django.db.models.signals import post_save

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    # When new user is created, profile is also created
    if created:
        Profile.objects.create(user=instance)