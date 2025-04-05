from django.contrib import admin
from .models import *
# Register your models here.


class detail_view_cart(admin.ModelAdmin):
    list_display = ['user','date_added']


admin.site.register(Cart,detail_view_cart)

class detail_view_cart_item(admin.ModelAdmin):
    list_display = ['product','cart','quantity','is_active']

admin.site.register(CartItem,detail_view_cart_item)


admin.site.register(order_status)

class detailed_transaction_history(admin.ModelAdmin):
    list_display=['user','old_product','old_product_price','old_product_quantity','date_purchased']

admin.site.register(Transactions_history,detailed_transaction_history)