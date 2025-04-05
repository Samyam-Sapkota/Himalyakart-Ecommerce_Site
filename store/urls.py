
from django.urls import path
from .views import store_views,product_details

urlpatterns = [
    path('',store_views,name="store_view"),
    path('product_details/',product_details,name="product_details"),
    path('<slug:category_slug>/',store_views,name="store_by_cat"),
    path('<slug:category_slug>/<slug:product_slug>/',product_details,name="product_details"),
] 
