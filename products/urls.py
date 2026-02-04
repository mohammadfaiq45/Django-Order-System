from django.urls import path
from . import views

urlpatterns = [
     path('admin/', views.admin_product_list, name='admin_product_list'),
    path('admin/add/', views.product_add, name='product_add'),
    path('admin/edit/<uuid:id>/', views.product_edit, name='product_edit'),
    path('admin/delete/<uuid:id>/', views.product_delete, name='product_delete'),


    path('customer/', views.customer_product_list, name='customer_product_list'),
]


