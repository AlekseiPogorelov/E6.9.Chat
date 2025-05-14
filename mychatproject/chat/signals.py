from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import Profile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, display_name=instance.username)
    else:
        try:
            instance.profile.save()
        except ObjectDoesNotExist:
            # Профиль не существует - создаём его
            Profile.objects.create(user=instance, display_name=instance.username)