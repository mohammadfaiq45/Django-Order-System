from django.shortcuts import render, redirect, get_object_or_404
from users.models import User
from products.models import Product
from .models import Order, OrderItem


def order_list(request):
    orders = Order.objects.all()
    return render(request, 'orders/order_list.html', {'orders': orders})


def order_accept(request, id):
    order = get_object_or_404(Order, id=id)
    order.status = 'accepted'
    order.rejection_reason = 'Accepted'
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


def order_success(request):
    return render(request, 'orders/order_success.html')

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    qty = int(request.POST.get('quantity', 1))

    cart = request.session.get('cart', {})

    if str(product.id) in cart:
        cart[str(product.id)] += qty
    else:
        cart[str(product.id)] = qty

    request.session['cart'] = cart
    return redirect('customer_product_list')

def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []

    for product_id, qty in cart.items():
        product = Product.objects.get(id=product_id)
        cart_items.append({
            'product': product,
            'quantity': qty
        })

    return render(request, 'orders/cart.html', {
        'cart_items': cart_items
    })


def checkout(request):
    users = User.objects.filter(is_admin=False)
    cart = request.session.get('cart', {})

    if request.method == 'POST':
        user_id = request.POST.get('user')
        address = request.POST.get('address')
        phone_no = request.POST.get('phone_no')
        special_instructions = request.POST.get('special_instructions', '')

        user = User.objects.get(id=user_id)

        order = Order.objects.create(
            user=user,
            address=address,
            phone_no=phone_no,
            special_instructions=special_instructions
        )

        for product_id, qty in cart.items():
            OrderItem.objects.create(
                order=order,
                product_id=product_id,
                quantity=qty
            )

        request.session['cart'] = {}
        return redirect('order_success')

    cart_items = []
    for product_id, qty in cart.items():
        product = Product.objects.get(id=product_id)
        cart_items.append({'product': product, 'quantity': qty})

    return render(request, 'orders/checkout.html', {
        'cart_items': cart_items,
        'users': users
    })
