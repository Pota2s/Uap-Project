from django.db import models
from accounts.models import CustomUser

# Create your models here.
class Store(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32,default="",blank=False)
    description = models.CharField(max_length=2048,default="",blank=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)

class StoreMember(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    store = models.ForeignKey(Store,on_delete=models.CASCADE,null=True)

class Product(models.Model):
    store = models.ForeignKey(Store, on_delete= models.CASCADE)
    name = models.CharField(max_length=32,default="",blank=False)
    cost = models.FloatField(null=True,default=0)
    description = models.CharField(max_length=2048,default="",blank=True)
    thumbnail = models.CharField(max_length=1024,default="",blank=True)
