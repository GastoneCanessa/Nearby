from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.contrib.gis.geos import fromstr
from geopy.geocoders import Nominatim
from groceries.storage_backend import PublicMediaStorage


class Greengrocer(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    user = models.OneToOneField(User(), on_delete=models.CASCADE)
    email = models.EmailField(max_length=254, unique=True)
    tel = models.PositiveIntegerField(default=0)   
    city = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    zip_code = models.PositiveIntegerField()
    location = models.PointField()
    
    def __str__(self):
        return self.name

    def location(self):
        geolocator = Nominatim(user_agent="nearby_greengrocer")
        location = geolocator.geocode(f'{self.address}, {self.city}')
        self.location = fromstr(
            f'POINT({location.latitude} {location.longitude})', srid=4326
            )

    def save(self, *args, **kwargs):
        self.location()
        super().save(*args, **kwargs)  # Call the "real" save() method.
        

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    greengrocer = models.ForeignKey(Greengrocer, on_delete=models.CASCADE)
    immage_url = models.FileField(storage=PublicMediaStorage(), default=None)
    date_posted = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title