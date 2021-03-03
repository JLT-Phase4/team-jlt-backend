from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms
from django.core.validators import MaxValueValidator

class User(AbstractUser):
    USER_TYPE_CHOICES = (
      (1, 'Captain'),
      (2, 'Member'),
  )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=2)
    avatar = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.username

class Team(models.Model):
    name = models.CharField(max_length=100, null=False)
    slogan = models.TextField(max_length=1000, null=True)
    captain = models.ForeignKey('User', on_delete=models.CASCADE, related_name='parent', null=True, verbose_name="username")
    members = models.ManyToManyField('User', related_name='teams', blank=True)
    theme_song = models.CharField(max_length=500, null=True, blank=True)
    background_image = models.CharField(max_length=500, null=True)
    dashboard_style = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Chore(models.Model):
    
    name = models.CharField(max_length=300)
    detail = models.TextField(max_length=1000)
    points = models.PositiveIntegerField(validators=[MaxValueValidator(10)], default=0)
    team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='chores')
    

    def __str__(self):
        return f'{self.name}'

class Assignment(models.Model):
    
    CHORE_TYPE_CHOICES = [
        ("MONDAY", 'Monday'),
        ("TUESDAY", 'Tuesday'),
        ("WEDNESDAY", 'Wednesday'),
        ("THURSDAY", 'Thursday'),
        ("FRIDAY", 'Friday'),
        ("SATURDAY", 'Saturday'),
        ("SUNDAY", 'Sunday'),
        ("ANYDAY", 'Anyday'),
    ]
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="assignments")
    chore = models.ForeignKey('Chore', on_delete=models.CASCADE, related_name='chores')
    comment = models.TextField(max_length=1000)
    complete = models.BooleanField(default=False)
    assignment_type = models.CharField(max_length= 10, choices=CHORE_TYPE_CHOICES, default='ANYDAY')
    

    def __str__(self):
        return f'{self.user} , {self.chore}'

class Pod(models.Model):
    name = models.CharField(max_length=500, null=False)
    teams = models.ManyToManyField('Team', related_name='pods')

    def __str__(self):
        return self.name


class Notification(models.Model):

    NOTIFICATION_TYPE_CHOICES = [
        ("MONDAY", 'Monday'),
        ("TUESDAY", 'Tuesday'),
        ("WEDNESDAY", 'Wednesday'),
        ("THURSDAY", 'Thursday'),
        ("FRIDAY", 'Friday'),
        ("SATURDAY", 'Saturday'),
        ("SUNDAY", 'Sunday'),
        ("ANYDAY", 'Anyday'),
    ]
    feed = models.ForeignKey('Feed', on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user', blank=True, null=True)
    target = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True)
    message = models.CharField(max_length=200, blank=False)
    emoji = models.CharField(max_length=100, blank=True)
    notification_type = models.CharField(max_length= 10, choices= NOTIFICATION_TYPE_CHOICES, default='ANYDAY')

    def __str__(self):
        return self.message


class Feed(models.Model):
    pod = models.ForeignKey('Pod', on_delete=models.CASCADE, null=True, related_name='feed')
    team = models.ForeignKey('Team', on_delete=models.CASCADE, null=True, related_name='feed')
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, related_name='feed')
    # def __str__(self):
    #     return self.pod