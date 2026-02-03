from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('accept/<int:id>/', views.order_accept, name='order_accept'),
    path('reject/<int:id>/', views.order_reject, name='order_reject'),
]
