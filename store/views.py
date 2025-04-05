from django.shortcuts import render,get_object_or_404,HttpResponse,redirect
from .models import Product
from category.models import Categories
from django.contrib import messages

# Create your views here.
def store_views(request,category_slug=None):
   category_obj=None
   available_products=None

   min_price =request.GET.get("min_price")
   max_price = request.GET.get("max_price")

   if (category_slug!=None) :
      category_obj = get_object_or_404(Categories,Cat_Slug=category_slug)
      available_products=Product.objects.all().filter(category=category_obj)
      no_of_products=available_products.count()

   else:
      available_products = Product.objects.all()
      no_of_products=available_products.count()

   if min_price and max_price:
      min_price = int(request.GET.get("min_price"))
      max_price = int(request.GET.get("max_price"))
      if max_price ==30000:
         available_products = Product.objects.all().filter(product_price__gte=min_price)
         no_of_products=available_products.count()
      else:
         if max_price < min_price :
            messages.warning(request, 'Max Price <= Min Price')
            return redirect('store_view')      
      
         else :
            available_products = Product.objects.all().filter(product_price__gte=min_price , product_price__lte=max_price)
            no_of_products=available_products.count()
      


   context = {'products':available_products,'no_of_products':no_of_products}
   return render(request,'store/store.html',context)


def product_details (request,category_slug=None,product_slug=None):
   if (category_slug!=None) :
      product_detail=Product.objects.filter(is_available=True,product_slug=product_slug)
   else:
      return HttpResponse('Product not available')
   context = {'product_detail':product_detail}
   return render(request,'store/product_details.html',context)