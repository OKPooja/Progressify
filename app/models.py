from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50, null=True)
    lastname = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    bio = models.CharField(max_length=254, default='Heyy I am new to Progressify')
    phoneno =   models.IntegerField(blank=True, null=True)
    designation = models.CharField(max_length=20)
    dateOfBirth = models.DateField(null = True)
    email = models.EmailField(null=True,max_length=254)

    def __str__(self):
        return f'{self.user.username}'


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    time = models.DateTimeField()


class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)


class Quota(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sleep = models.IntegerField(default=0)
    study = models.IntegerField(default=0)
    date = models.DateField(default=timezone.now)
