from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    designation = models.CharField(max_length=20)

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
    sleep = models.IntegerField(null=True)
    study = models.IntegerField(null=True)
