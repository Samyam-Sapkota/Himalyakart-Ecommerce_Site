from django.contrib import admin
from .models import Product


class Product_display_more(admin.ModelAdmin):
    list_display = ('product_name','product_slug','product_price','category','Items_in_stock')
    prepopulated_fields = {"product_slug":('product_name',)}
    list_filter =('product_price',)
# Register your models here.
admin.site.register(Product,Product_display_more)


