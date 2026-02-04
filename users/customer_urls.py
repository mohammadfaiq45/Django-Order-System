from django.urls import path
from products.views import CustomerProductListView
from orders.views import AddToCartView, ViewCartView, CheckoutView, OrderSuccessView

urlpatterns = [
    path('products/', CustomerProductListView.as_view(), name='customer_product_list'),

    path('cart/add/<uuid:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', ViewCartView.as_view(), name='view_cart'),

    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('success/', OrderSuccessView.as_view(), name='order_success'),
]
