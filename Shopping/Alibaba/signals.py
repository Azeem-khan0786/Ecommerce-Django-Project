from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import ProfileModel

@receiver(post_save , sender = User)
def create_profile(instance,sender,created,**kwargs):
    if created:
        ProfileModel.objects.create(user = instance,name=instance.username,
                                    email = instance.email)
