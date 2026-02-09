from django.urls import path
from products.views import AdminProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView
from orders.views import AdminOrderView, AdminOrderActionView

urlpatterns = [
    path('products/', AdminProductListView.as_view(), name='admin_product_list'),
    path('products/add/', ProductCreateView.as_view(), name='product_add'),
    path('products/edit/<uuid:id>/', ProductUpdateView.as_view(), name='product_edit'),
    path('products/delete/<uuid:id>/', ProductDeleteView.as_view(), name='product_delete'),

    path('orders/', AdminOrderView.as_view(), name='order_list'),
    path('orders/action/<int:id>/<str:action>/', AdminOrderActionView.as_view(), name='order_action'),
]
