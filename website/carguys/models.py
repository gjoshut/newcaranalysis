from django.db import models
from datetime import date

class Presale(models.Model):
    Picture_Count = models.CharField(max_length = 200)
    CR = models.CharField(max_length = 200)
    Year = models.IntegerField(default = 0)
    Make = models.CharField(max_length = 200)
    Model = models.CharField(max_length = 200)
    Style =  models.CharField(max_length = 200)
    Odometer = models.IntegerField(default = 0)
    Color = models.CharField(max_length = 200)
    Stock = models.IntegerField(default = 0)
    Grade = models.CharField(max_length = 200)
    Sale_Date = models.CharField(max_length = 200)
    Run_number = models.CharField(max_length = 200)
    Lane = models.CharField(max_length = 200)
    Lot = models.CharField(max_length = 200)
    VIN = models.CharField(max_length = 200)
    Day = models.DateField(default = date.today())
    Predicted_Price = models.FloatField(default = 0, null = True)
    class Meta:
        ordering = ('Model',)

class Postsales(models.Model):
    Picture_Count = models.CharField(max_length = 200)
    CR = models.CharField(max_length = 200)
    Year = models.IntegerField(default = 0)
    Make = models.CharField(max_length = 200)
    Model = models.CharField(max_length = 200)
    Style =  models.CharField(max_length = 200)
    Odometer = models.IntegerField(default = 0)
    Color = models.CharField(max_length = 200)
    Stock = models.CharField(max_length = 200)
    Grade = models.CharField(max_length = 200)
    Sale_Date = models.CharField(max_length = 200)
    Lane = models.CharField(max_length = 200)
    Run_number = models.CharField(max_length = 200)
    Price = models.FloatField(default = 0)
