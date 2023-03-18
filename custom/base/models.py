from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


class CustomUser(AbstractUser):
    name=models.CharField(max_length=100,null=True)
    email=models.EmailField(unique=True,null=True)
    username=models.CharField(max_length=100,null=True,blank=True,unique=False)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['name']



class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)


    def __str__(self):
        return self.user.email

@receiver(post_save, sender=CustomUser)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()

