from django.urls import path
from .views import productView,storeView

urlpatterns = [
    path("product/<int:product_id>",productView, name="product"),
    path("<int:store_id>",storeView,name="store")
    
]