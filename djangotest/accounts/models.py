from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    pass

    wallet = models.FloatField(null=True,default=0.0)

    def __repr__(self):
        return repr(super())
    
    def __str__(self):
        return self.username