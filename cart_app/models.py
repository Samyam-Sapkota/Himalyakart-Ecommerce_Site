from django.db import models

# Create your models here.
from django.db import models
from store.models import Product
from django.contrib.auth.models import User

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Cart-{self.user.username}"

class CartItem(models.Model):
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.product)
    

class order_status(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    order_is_completed = models.BooleanField(default=False)
    order_cancelled = models.BooleanField(default=False) 


    def __str__(self):
        return str(self.cart)


class Transactions_history(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    # cart_item = models.ForeignKey(CartItem,on_delete=models.CASCADE)
    # order_status = models.ForeignKey(order_status,on_delete=models.CASCADE)
    old_product = models.CharField(max_length=100)
    old_product_price = models.IntegerField()
    old_product_quantity = models.IntegerField()
    date_purchased = models.DateTimeField(auto_now=True)
