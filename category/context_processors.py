from .models import Categories
from store.models import Product



def return_cat (request):
    cat_obj1 = Categories.objects.all()
    return {"cat_obj1":cat_obj1}

def return_product (request):
    product_obj1 = Product.objects.all()
    return {"product_obj1":product_obj1}





