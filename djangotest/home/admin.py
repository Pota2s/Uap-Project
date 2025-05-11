from django.contrib import admin

from .models import Product,User,Store
# Register your models here.
admin.site.register(Product)
admin.site.register(User)
admin.site.register(Store)