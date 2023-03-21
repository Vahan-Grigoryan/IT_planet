from django.utils import timezone as tz
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator



class Account(AbstractUser):
    username = models.CharField('username', unique=True, max_length=150, blank=True, null=True)
    email = models.EmailField("Email address", unique=True)
    first_name = models.CharField("first name", max_length=150, null=False, default='F1')
    last_name = models.CharField("last name", max_length=150, null=False, default='L1')


    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'ACCOUNT'
        verbose_name_plural = 'ACCOUNTS'

class LocationPoint(models.Model):
    latitude = models.FloatField( validators=[MinValueValidator(-90), MaxValueValidator(90)], unique=True )
    longitude = models.FloatField( validators=[MinValueValidator(-180), MaxValueValidator(180)], unique=True )

    def __str__(self):
        return f'latitude:{self.latitude}, longitude:{self.longitude}'

class AnimalVisitedLocation(models.Model):
    date_time_of_visit_location_point = models.DateTimeField()
    location_point = models.ForeignKey(LocationPoint, on_delete=models.SET_NULL, null=True, related_name='visited_location_point')

    def __str__(self):
        return f'Visited location: ({self.locationPoint})'

class Animal(models.Model):
    gender_choices = ('MALE', 'MALE'), ('FEMALE', 'FEMALE'), ('OTHER', 'OTHER')
    lifeStatus_choices = ('ALIVE', 'ALIVE'), ('DEAD', 'DEAD')
    deathDateTime_choices = (tz.now().isoformat(), tz.now().isoformat()),

    weight = models.FloatField()
    length = models.FloatField()
    height = models.FloatField()
    gender = models.CharField(choices=gender_choices, max_length=10, null=False)
    lifeStatus = models.CharField(choices=lifeStatus_choices, max_length=10, default='ALIVE')
    chipping_date_time = models.DateTimeField(default=tz.now)
    chipper = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='animals')
    chipping_location = models.ForeignKey(LocationPoint, on_delete=models.DO_NOTHING, related_name='animals')
    visited_locations = models.ManyToManyField(AnimalVisitedLocation, related_name='visited_animals')
    deathDateTime = models.CharField(choices=deathDateTime_choices, max_length=50, null=True, blank=True, default=None)
    #animal_type = relation to AnimalType

    def __str__(self):
        return f"Animal: lifeStatus={self.lifeStatus}, deathDateTime={self.deathDateTime}"



class AnimalType(models.Model):
    type = models.CharField(max_length=100, unique=True)
    animals = models.ManyToManyField(Animal, related_name='animalTypes', blank=True)

    def __str__(self):
        return self.type

