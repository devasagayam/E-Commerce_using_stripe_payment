from django.contrib import auth
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.conf import settings
from autoslug import AutoSlugField
from django.core.validators import RegexValidator

alpha = RegexValidator(r'^[a-zA-Z ]*$', 'Only alphabets characters are allowed.')



Gender=(
    ('male','Male'),
    ('female','Female'),
)
class User(auth.models.User, auth.models.PermissionsMixin):

    def __str__(self):
        return "@{}".format(self.username)


class Profile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    status=models.BooleanField(default=0)
    Name=models.CharField(max_length=50, blank=True, null=True,validators=[alpha])
    DOB=models.DateTimeField(blank=True, null=True)
    gender=models.CharField("Gender",max_length=20,choices=Gender,default=[0][0])
    phone=PhoneNumberField(blank=True, null=True)
    image=models.ImageField(upload_to='photos/',blank=True,)


def profile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
post_save.connect(profile_receiver, sender=get_user_model())
