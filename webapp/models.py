from django.db import models

#1 Model Trip ment for displaying dynamic data about expeditions organized by the agency
class Trip(models.Model):
    trip_id = models.AutoField(primary_key=True)
    trip_name = models.CharField(max_length=256)
    trip_description = models.TextField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)


    def __str__(self):
        return f"{self.trip_name}"
# 2 Model Guide linked with Trip model
class Guide(models.Model):
    guide_id = models.AutoField(primary_key=True)
    guide_name = models.CharField(max_length=256)
    guided_trips = models.ManyToManyField('Trip', blank=True)

    def __str__(self):
        return f"{self.guide_name}"

# 3 Model Customer linked with Trip model to easily determine who is going where
class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    customer_first_name = models.CharField(max_length=64, null=True, blank=True)
    customer_last_name = models.CharField(max_length=64, null=True, blank=True)
    customer_email = models.EmailField(null=True, blank=True)
    customer_phone = models.IntegerField(null=True, blank=True)
    customer_trips = models.ManyToManyField('Trip', blank=True)

    def __str__(self):
        return f"{self.customer_first_name} {self.customer_last_name}"

"""
4 Model inherits from Trip, ment for internal administration, to show how 
many people are interested in particular travel and who is assigned to guide them
"""
class TripDetail(Trip):
    customers = models.ManyToManyField('Customer', blank=True)
    guides = models.ManyToManyField('Guide', blank=True)



