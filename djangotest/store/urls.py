from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
urlpatterns = [
    path("<int:store_id>/products/<int:product_id>",views.productView, name="product"),
    path("<int:store_id>",views.storeView,name="store"),
    path("<int:store_id>/add",views.productCreateView, name="product_create"),
    path("<int:store_id>/edit",views.storeEditView, name="store_edit"),
    path("create",views.storeCreateView,name="store_create"),
    path("<int:store_id>/products/<int:product_id>/edit",views.productEditView, name="product_edit"),
    path("<int:store_id>/products/<int:product_id>/wishlist",views.addToWishList, name="add_to_wishlist"),
    path("<int:store_id>/products/<int:product_id>/unwishlist",views.removeFromWishList, name="remove_from_wishlist"),
    path("",views.globalStoreView, name="global_store"),
    path("<int:store_id>/products/<int:product_id>/add_to_cart",views.addToCart, name="add_to_cart"),
    path("<int:store_id>/products/<int:product_id>/remove_from_cart",views.removeFromCart, name="remove_from_cart"),
    path("cart",views.cartView, name="cart"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)