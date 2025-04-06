from django.shortcuts import render,redirect,HttpResponse
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from store.models import Product
from .models import Cart,CartItem,order_status,Transactions_history
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail



stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def cart_detail(request, total=0, quantity=0, tax=0, cart_items=None):
   
    tax_amount = final_amount = 0
    try:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.product_price * cart_item.quantity) 
            quantity += cart_item.quantity
        tax_amount = round(total * 0.13, 4)
        final_amount = round(total + tax_amount, 2)
    except ObjectDoesNotExist:
        pass
    context = {
        "total": total,
        "quantity": quantity,
        "cart_items": cart_items,
        'tax_amount': tax_amount,
        "final_amount": final_amount,
    }
    return render(request, 'cart/cart1.html', context)

@login_required
def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1 
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1,
                    )
    
    return redirect('cart_detail')

@login_required
def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.get(product=product, cart=cart)
   
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_detail')

@login_required
@csrf_exempt
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        
        if not cart_items.exists():
            messages.warning(request,"No items in cart")
            return redirect('cart_detail')

        # Calculate totals
        total = sum(item.product.product_price * item.quantity for item in cart_items)
        quantity = sum(item.quantity for item in cart_items)
        sample_tax = round(total * 0.13, 4)
        sample_total = round(total + sample_tax, 2)

        # Create line items for each product
        line_items = []
        for cart_item in cart_items:
            product = cart_item.product
            product_image_url = request.build_absolute_uri(product.product_image.url)
           
            line_items.append({
                'price_data': {
                    'currency': 'npr',
                    'product_data': {
                        'name': str(product),
                        'images': [product_image_url],  # Add product image
                        
                    },
                    'unit_amount': int(product.product_price * 100),
                },
                'quantity': cart_item.quantity,
            })

        
        line_items.append({
            'price_data': {
                'currency': 'npr',
                'product_data': {
                    'name': 'Tax (13%)',
                },
                'unit_amount': int(sample_tax * 100),
            },
            'quantity': 1,
        })

        if request.method == 'POST':
            # domain = request.build_absolute_uri('/').strip('/')
            domain = f"{request.scheme}://{request.get_host()}" 
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=f"{domain}/cart/success/",
                cancel_url=f"{domain}/cart/cancel/",
            )
            return JsonResponse({'checkout_session_id': session.id})

        context = {
            "sample_price": total,
            "quantity": quantity,
            "cart_items": cart_items,
            'sample_tax': sample_tax,
            "sample_total": sample_total,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        }
        return render(request, 'cart/checkout.html', context)

    except Cart.DoesNotExist:
        return HttpResponse('No items in Cart')





@login_required
def sucess_page(request):
    cart = Cart.objects.get(user=request.user)
    if order_status.objects.filter(cart=cart).exists: 
        order_status_obj = order_status.objects.filter(cart=cart)
        order_status_obj.update(order_is_completed = True,order_cancelled = False)
    else:
        order_status_obj = order_status.objects.filter(cart=cart)
        order_status_obj.create(cart=cart,order_is_completed=True,order_cancelled = False)
   

    recipient_email = request.user.email
    subject = 'Product order sucessfull-HimalayaKart'
    message = """Thank you for placing your order! We are happy to have you with us. Your order will be delivered anytime by 2-3 days from now, if you have any complaints please contact us or email us . 
    
                -Thank you-himalayakart-Team. """
    from_email = settings.EMAIL_HOST_USER  
    try:
        send_mail(subject, message, from_email, [recipient_email])
        messages.success(request, 'Your order was successful! Please check your email')
    except Exception as e:
        messages.warning(request, 'Your order was successful but your email was probably not sent')



    cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    
 

    for item in cart_items:
        Transactions_history.objects.create(
        user=request.user,
        old_product=item.product.product_name,
        old_product_price = item.product.product_price,
        old_product_quantity = item.quantity,
        )

    # Clear cart items
    cart_items.delete()
    order_status_obj.delete()   
    return redirect('home_view')

@login_required
def cancel_page(request):

    cart = Cart.objects.get(user=request.user)
    if order_status.objects.filter(cart=cart).exists: 
        order_status_obj = order_status.objects.filter(cart=cart)
        order_status_obj.update(order_is_completed = False,order_cancelled = True)
    else:
        order_status_obj = order_status.objects.filter(cart=cart)
        order_status_obj.create(cart=cart,order_is_completed=False,order_cancelled = True)
    
    messages.warning(request, 'Your order was cancelled!')
    return redirect('checkout')


@login_required
def transaction_history(request):
    transaction_object1 = Transactions_history.objects.all().filter(user=request.user)
   
    overall_price=0
    for items_price in transaction_object1:
        overall_price += (items_price.old_product_price * items_price.old_product_quantity)
    tax_amount = round(overall_price * 0.13, 4)
    final_amount = round(overall_price + tax_amount, 2)
    context={"transaction_object1":transaction_object1,"overall_price":overall_price,"tax_amount":tax_amount,"final_amount":final_amount}
    return render(request,"others/dashboard.html",context)
    