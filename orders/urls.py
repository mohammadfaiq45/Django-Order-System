from django.urls import path
from . import views

urlpatterns = [
    path('admin/', views.order_list, name='order_list'),
    path('admin/accept/<int:id>/', views.order_accept, name='order_accept'),
    path('admin/reject/<int:id>/', views.order_reject, name='order_reject'),

    path('success/', views.order_success, name='order_success'),
    path('cart/add/<uuid:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),

]
