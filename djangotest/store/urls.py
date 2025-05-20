from django.urls import path
from . import views
urlpatterns = [
    path("<int:store_id>/products/<int:product_id>",views.productView, name="product"),
    path("<int:store_id>",views.storeView,name="store"),
    path("<int:store_id>/add",views.productCreateView, name="product_create"),
    path("<int:store_id>/edit",views.storeEditView, name="store_edit"),
    path("create",views.storeCreateView,name="store_create"),
    path("<int:store_id>/products/<int:product_id>/edit",views.productEditView, name="product_edit"),
]