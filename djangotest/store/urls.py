from django.urls import path
from . import views
urlpatterns = [
    path("product/<int:product_id>",views.productView, name="product"),
    path("<int:store_id>",views.storeView,name="store"),
    path("<int:store_id>/edit",views.storeEditView, name="store_edit"),
    path("register",views.register)
]