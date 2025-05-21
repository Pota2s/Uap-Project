from django.db import models
from accounts.models import CustomUser

# Create your models here.
class Store(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32,default="",blank=False)
    description = models.CharField(max_length=2048,default="",blank=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    thumbnail = models.ImageField(upload_to='images/thumbnails/',default="images/default.svg",blank=True)

class StoreMember(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    store = models.ForeignKey(Store,on_delete=models.CASCADE,null=True)

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    store = models.ForeignKey(Store, on_delete= models.CASCADE)
    name = models.CharField(max_length=32,default="",blank=False)
    price = models.FloatField(null=True,default=0)
    description = models.CharField(max_length=2048,default="",blank=True)
    thumbnail = models.ImageField(upload_to='images/products/',default="images/default.svg",blank=True)

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class WishList(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)