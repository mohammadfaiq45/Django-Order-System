from django.shortcuts import render, redirect, get_object_or_404
from .models import Order

def order_list(request):
    orders = Order.objects.all()
    return render(request, 'orders/order_list.html', {'orders': orders})


def order_accept(request, id):
    order = get_object_or_404(Order, id=id)
    order.status = 'accepted'
    order.save()
    return redirect('order_list')


def order_reject(request, id):
    order = get_object_or_404(Order, id=id)

    if request.method == 'POST':
        order.status = 'rejected'
        order.rejection_reason = request.POST['rejection_reason']
        order.save()
        return redirect('order_list')

    return render(request, 'orders/order_reject.html', {'order': order})

