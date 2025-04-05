from django.db import models
from django.urls import reverse
# Create your models here.


class Categories (models.Model):
    Cat_Name= models.CharField(max_length=20)
    Cat_Slug = models.SlugField(max_length=30)
    Cat_Description = models.TextField(max_length=200)
    Cat_Images = models.ImageField(upload_to='media/category/')
    Date_Created =models.DateTimeField(auto_now_add=True)
    Date_Modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.Cat_Name

    def get_url_test (self):
         return reverse('store_by_cat',args=[self.Cat_Slug])          # name of the url and the field you want to return back 
    

    class Meta:
        verbose_name_plural='categories'