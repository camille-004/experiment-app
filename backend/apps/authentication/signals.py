from typing import Any

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(
    sender: type[User], instance: User, created: bool, **kwargs: Any
) -> None:
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(
    sender: type[User], instance: User, **kwargs: Any
) -> None:
    instance.authentication_userprofile.save()
