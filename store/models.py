from django.db import models
from category.models import Categories
from django.urls import reverse

# Create your models here.

class Product(models.Model):
    product_name=models.CharField(max_length=50)
    product_slug=models.CharField(max_length=50)
    product_description = models.TextField(max_length=500)
    product_image = models.ImageField(upload_to='media/products/')
    product_price = models.IntegerField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    Items_in_stock = models.IntegerField(default=0)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse ('product_details',args=[self.category.Cat_Slug,self.product_slug])

    def __str__(self):
        return self.product_name


