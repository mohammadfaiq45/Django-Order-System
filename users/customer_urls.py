from django.urls import path
from orders.views import CustomerOrderView
from products.views import CustomerProductListView

urlpatterns = [
    path('products/', CustomerProductListView.as_view(), name='customer_product_list'),
    path('cart/', CustomerOrderView.as_view(), {'page': 'cart'}, name='view_cart'),
    path('checkout/', CustomerOrderView.as_view(), {'page': 'checkout'}, name='checkout'),
    path('success/', CustomerOrderView.as_view(), {'page': 'success'}, name='order_success'),
    path('cart/add/<uuid:product_id>/', CustomerOrderView.as_view(), {'action': 'add'}, name='add_to_cart'),
]
