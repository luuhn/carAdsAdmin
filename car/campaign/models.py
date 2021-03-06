from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils.safestring import mark_safe
# Create your models here.


class Location(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Campaign(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    num_cars = models.DecimalField(max_digits=4, decimal_places=0)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    maxkm = models.IntegerField(blank=True, null=True,default=2100)
    def __str__(self):
        return self.name


class Car(models.Model):
    plate_num = models.CharField(max_length=10,unique=True)
    car_name = models.CharField(max_length=100,blank=True)
    car_seat = models.CharField(max_length=2,blank=True)
    car_color = models.CharField(max_length=10,blank=True)
    driver_name = models.CharField(max_length=100,blank=True)
    phone = models.CharField(max_length=15,blank=True)
    bank_name = models.CharField(max_length=100,blank=True)
    bank_branch = models.CharField(max_length=100,blank=True)
    bank_account = models.CharField(max_length=15,blank=True)
    password = models.CharField(max_length=50,default="123456")
    status = models.BooleanField(blank=True)
    def __str__(self):
        return self.plate_num

class Report(models.Model):
    name = models.CharField(max_length=200)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class ReportImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    image_odo = models.URLField(max_length=500,blank=True)
    image_drive = models.URLField(max_length=500,blank=True)
    image_pass = models.URLField(max_length=500,blank=True)
    image_plate = models.URLField(max_length=500,blank=True)
    date = models.DateField(blank=True, default=datetime.date.today)
    odo_aproved = models.BooleanField(blank=True,default=False)
    drive_aproved = models.BooleanField(blank=True,default=False)
    pass_aproved = models.BooleanField(blank=True,default=False)
    plate_aproved = models.BooleanField(blank=True,default=False)
    def image_odo_thumbnail(self):
        return mark_safe('<img src="%s" width="auto" height="50"/>' % (self.image_odo))
    def image_drive_thumbnail(self):
        return mark_safe('<img src="%s" width="auto" height="50"/>' % (self.image_drive))
    def image_pass_thumbnail(self):
        return mark_safe('<img src="%s" width="auto" height="50"/>' % (self.image_pass))
    def image_plate_thumbnail(self):
        return mark_safe('<img src="%s" width="auto" height="50"/>' % (self.image_plate))


class CampaignCar(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    deviceid = models.CharField(max_length=15)

class CampaignKpi(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    totalDistance = models.DecimalField(max_digits=15, decimal_places=2)
    province = models.CharField(max_length=100)
    district = models.CharField(max_length=200)

class CampaignHourly(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    totalDistance = models.DecimalField(max_digits=15, decimal_places=2)
    hour = models.IntegerField()

class CarKpi(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    totalDistance = models.DecimalField(max_digits=15, decimal_places=2)
    impression = models.DecimalField(max_digits=15, decimal_places=0, null=True)
    date = models.DateField()
    province = models.CharField(max_length=100)
    def plate(self):
        return self.car.plate_num

class UserCampaign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
