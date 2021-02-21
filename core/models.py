from django.db import models
from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField

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
    slogan = models.TextField(max_length=1000, null=False)
    captain = models.ForeignKey('User', on_delete=models.CASCADE, related_name='parent')
    members = models.ManyToManyField('User', related_name='kids', blank=True)
    theme_song = models.CharField(max_length=500, null=True, blank=True)
    background_image = models.CharField(max_length=500, null=True)
    dashboard_style = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Chore(models.Model):
    MONDAY = 'MD'
    TUESDAY = 'TUE'
    WEDNESDAY = 'WED'
    THURSDAY = 'THUR'
    FRIDAY = 'FRI'
    SATURDAY = 'SAT'
    SUNDAY = 'SUN'
    ANYDAY = 'ANY'
    CHORE_TYPE_CHOICES = [
        (MONDAY, 'Monday'),
        (TUESDAY, 'Tuesday'),
        (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'),
        (FRIDAY, 'Friday'),
        (SATURDAY, 'Saturday'),
        (SUNDAY, 'Sunday'),
        (ANYDAY, 'Anyday'),
    ]
    
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="chores")
    name = models.CharField(max_length=300)
    detail = models.TextField(max_length=1000)
    chore_type = MultiSelectField(
        max_length=50,
        choices=CHORE_TYPE_CHOICES,
        default=ANYDAY,
        max_choices=7,
        
    )

    def __str__(self):
        return f'{self.name} , {self.user}'

class Record(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="records")
    chore = models.ForeignKey('Chore', on_delete=models.CASCADE)
    date = models.DateField(verbose_name="date-of-record")
    comment = models.TextField(max_length=1000)
    complete = models.BooleanField(default=False)
    

    def __datetime__(self):
        return self.date

class Pod(models.Model):
    name = models.CharField(max_length=500, null=False)
    teams = models.ManyToManyField('Team', related_name='teams')

    def __str__(self):
        return self.name

