from unicodedata import category
from django.db import models

class Sales(models.Model):
    country = models.CharField(max_length=50)
    orderID = models.IntegerField(max_length=50)
    totalCost= models.DecimalField(max_digits=1000, decimal_places=3)
    category = models.CharField(max_length=50, blank=True)
    