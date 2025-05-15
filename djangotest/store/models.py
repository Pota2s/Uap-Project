from django.db import models

# Create your models here.
class Store(models.Model):
    name = models.CharField(max_length=32,default="",blank=False)


class Product(models.Model):
    store = models.ForeignKey(Store, on_delete= models.CASCADE)
