from django.urls import path
from products.views import (AdminProductListView, ProductCreateView, ProductUpdateView,
ProductDeleteView)
from orders.views import (OrderListView, OrderAcceptView, OrderRejectView)

urlpatterns = [
    path('products/', AdminProductListView.as_view(), name='admin_product_list'),
    path('products/add/', ProductCreateView.as_view(), name='product_add'),
    path('products/edit/<uuid:id>/', ProductUpdateView.as_view(), name='product_edit'),
    path('products/delete/<uuid:id>/', ProductDeleteView.as_view(), name='product_delete'),

    path('orders/', OrderListView.as_view(), name='order_list'),
    path('orders/accept/<int:id>/', OrderAcceptView.as_view(), name='order_accept'),
    path('orders/reject/<int:id>/', OrderRejectView.as_view(), name='order_reject'),
]
