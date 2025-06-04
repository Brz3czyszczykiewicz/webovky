from django.core.validators import MaxValueValidator, MaxLengthValidator, MinLengthValidator
from django.db import models
from pathlib import Path
from django.conf import settings
from django.utils import timezone


#1 Model Trip ment for displaying dynamic data about expeditions organized by the agency
class Trip(models.Model):
    trip_id = models.AutoField(primary_key=True)
    trip_name = models.CharField(max_length=256)
    trip_short_description = models.TextField(null=True, blank=True)
    trip_description = models.TextField(null=True, blank=True)
    start_time = models.CharField(null=True, blank=True, max_length=30) #not date field at the clients request
    end_time = models.CharField(null=True, blank=True, max_length=30) #vague dates preferred - start of june
    price = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='', null=True, blank=True)

    @property
    def customer_count(self):
        """
        or 1 because first database entries i created had no customer_count making sum unfeasible
        using related name, goal of this property is to have reference in html to
        give rough idea of how many people have signed up
        """
        return sum((number.customer_count or 1) for number in self.customer_trip.all())

    @property
    #how many reservations were created
    def reservation_count(self):
        return self.customer_trip.all().count()

    @classmethod
    def get_directory_images(cls):
        stored_images = Path(settings.MEDIA_ROOT)
        if not stored_images:
            return []
        images = []
        for file in stored_images.iterdir():
            if file.is_file() and file.suffix.lower() in ('.jpg', '.jpeg', '.png'):
                images.append(f"{settings.MEDIA_URL}{file.name}")
        return images


    def __str__(self):
        return f"{self.trip_name}"

#2 created for trip to store multiple images
class TripImage(models.Model):
    relation = models.ForeignKey(Trip, related_name="trip_image", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="", null=True, blank=True)
    caption = models.CharField(max_length=64, null=True, blank=True)

    @classmethod
    def get_directory_images(cls):
        stored_images = Path(settings.MEDIA_ROOT)
        if not stored_images:
            return []
        images = []
        for file in stored_images.iterdir():
            if file.is_file() and file.suffix.lower() in ('.jpg', '.jpeg', '.png'):
                images.append(file.name)
        return images
        


    def __str__(self):
        return f"Image for{self.trip.trip_name}"

    





    
# 3 Model Guide linked with Trip model
class Guide(models.Model):
    guide_id = models.AutoField(primary_key=True)
    guide_name = models.CharField(max_length=256)
    guided_trips = models.ManyToManyField('Trip', blank=True)

    def __str__(self):
        return f"{self.guide_name}"

# 4 Model Customer linked with Trip model to easily determine who is going where
class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    customer_first_name = models.CharField(max_length=64, null=True, blank=True)
    customer_last_name = models.CharField(max_length=64, null=True, blank=True)
    customer_count = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(30)],)
    customer_email = models.EmailField(null=True, blank=True)
    customer_phone = models.CharField(max_length=14, null=True, blank=True, validators=[MinLengthValidator(9)])
    customer_message = models.TextField(null=True, blank=True)
    customer_trip = models.ForeignKey('Trip', on_delete=models.CASCADE,
                                      null=True, blank=True, related_name='customer_trip')
    created = models.DateTimeField(auto_now_add=True)
    @property
    def full_name(self):
        return f"{self.customer_first_name} {self.customer_last_name}"

    def __str__(self):
        return self.full_name

"""
5 Model inherits from Trip, ment for internal administration, to show how 
many people are interested in particular travel and who is assigned to guide them
"""
class TripDetail(Trip):
    customers = models.ManyToManyField('Customer', blank=True)
    guides = models.ManyToManyField('Guide', blank=True)

class CustomerAdmin(Customer):
    trips = models.ManyToManyField(Trip, blank=True)



