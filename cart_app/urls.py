from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('checkout/', views.checkout, name='checkout'),
    path('add_cart/<int:product_id>/', views.add_cart,name='add_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart,name='remove_from_cart'),
    path('success/',views.sucess_page,name="sucess_page"),
    path('cancel/',views.cancel_page,name="cancel_page"),
    path('transaction_history/',views.transaction_history,name="transaction_history"),

    
]