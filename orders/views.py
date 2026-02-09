from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from users.decorators import admin_required, customer_required
from users.models import User
from products.models import Product
from .models import Order, OrderItem


@method_decorator(admin_required, name='dispatch')
class AdminOrderView(View):
    template_name = 'orders/order_list.html'

    def get(self, request):
        orders = Order.objects.all()
        return render(request, self.template_name, {'orders': orders})


@method_decorator(admin_required, name='dispatch')
class AdminOrderActionView(View):

    def get(self, request, id, action):
        order = get_object_or_404(Order, id=id)
        if action == 'accept':
            for item in order.items.all():
                product = item.product
                if product.available_units < item.quantity:
                    order.status = 'rejected'
                    order.rejection_reason = f'Not enough stock for {product.name}'
                    order.save()
                    return redirect('order_list')

                product.available_units -= item.quantity
                product.save()

            order.status = 'accepted'
            order.rejection_reason = 'Accepted'
            order.save()
            return redirect('order_list')

        elif action == 'reject':
            return render(request, 'orders/order_reject.html', {'order': order})

    def post(self, request, id, action):
        order = get_object_or_404(Order, id=id)
        if action == 'reject':
            order.status = 'rejected'
            order.rejection_reason = request.POST.get('rejection_reason', 'No reason provided')
            order.save()
        return redirect('order_list')



@method_decorator(customer_required, name='dispatch')
class CustomerOrderView(View):

    def get(self, request, **kwargs):
        page = kwargs.get('page')
        cart = request.session.get('cart', {})
        cart_items = []
        for pid, qty in cart.items():
            product = get_object_or_404(Product, id=pid)
            cart_items.append({'product': product, 'quantity': qty})

        if page == 'cart':
            return render(request, 'orders/cart.html', {'cart_items': cart_items})

        if page == 'checkout':
            user = get_object_or_404(User, id=request.session['user_id'])
            return render(request, 'orders/checkout.html', {
                'cart_items': cart_items,
                'user': user
            })

        if page == 'success':
            return render(request, 'orders/order_success.html')

        return redirect('customer_product_list')


    def post(self, request, **kwargs):
        action = kwargs.get('action')
        if action == 'add':
            product_id = kwargs.get('product_id')
            product = get_object_or_404(Product, id=product_id)
            qty = int(request.POST.get('quantity', 1))
            cart = request.session.get('cart', {})
            cart[str(product.id)] = cart.get(str(product.id), 0) + qty
            request.session['cart'] = cart
            return redirect('view_cart')

        if kwargs.get('page') == 'checkout':
            user = get_object_or_404(User, id=request.session['user_id'])
            cart = request.session.get('cart', {})
            order = Order.objects.create(
                user=user,
                address=request.POST.get('address'),
                phone_no=request.POST.get('phone_no'),
                special_instructions=request.POST.get('special_instructions', '')
            )
            for pid, qty in cart.items():
                OrderItem.objects.create(
                    order=order,
                    product_id=pid,
                    quantity=qty
                )
            request.session['cart'] = {}
            return redirect('order_success')

        return redirect('customer_product_list')









# from django.shortcuts import render, redirect, get_object_or_404
# from django.views import View
# from django.views.generic import ListView
# from django.utils.decorators import method_decorator
# from users.decorators import admin_required, customer_required
# from users.models import User
# from products.models import Product
# from .models import Order, OrderItem


# @method_decorator(admin_required, name='dispatch')
# class OrderListView(ListView):
#     model = Order
#     template_name = 'orders/order_list.html'
#     context_object_name = 'orders'

# @method_decorator(admin_required, name='dispatch')
# class OrderAcceptView(View):
#     def get(self, request, id):
#         order = get_object_or_404(Order, id=id)

#         if order.status == 'accepted':
#             return redirect('order_list')

#         for item in order.items.all():
#             product = item.product
#             if product.available_units >= item.quantity:
#                 product.available_units -= item.quantity
#                 product.save()
#             else:
#                 order.status = 'rejected'
#                 order.rejection_reason = f'Not enough stock for {product.name}'
#                 order.save()
#                 return redirect('order_list')

#         order.status = 'accepted'
#         order.rejection_reason = 'Accepted'
#         order.save()

#         return redirect('order_list')

# @method_decorator(admin_required, name='dispatch')
# class OrderRejectView(View):
#     def get(self, request, id):
#         order = get_object_or_404(Order, id=id)
#         return render(request, 'orders/order_reject.html', {'order': order})

#     def post(self, request, id):
#         order = get_object_or_404(Order, id=id)
#         order.status = 'rejected'
#         order.rejection_reason = request.POST['rejection_reason']
#         order.save()
#         return redirect('order_list')

# @method_decorator(customer_required, name='dispatch')
# class OrderSuccessView(View):
#     def get(self, request):
#         return render(request, 'orders/order_success.html')

# @method_decorator(customer_required, name='dispatch')
# class AddToCartView(View):
#     def post(self, request, product_id):
#         product = get_object_or_404(Product, id=product_id)
#         qty = int(request.POST.get('quantity', 1))

#         cart = request.session.get('cart', {})
#         cart[str(product.id)] = cart.get(str(product.id), 0) + qty
#         request.session['cart'] = cart

#         return redirect('customer_product_list')

# @method_decorator(customer_required, name='dispatch')
# class ViewCartView(View):
#     def get(self, request):
#         cart = request.session.get('cart', {})
#         cart_items = []

#         for product_id, qty in cart.items():
#             product = get_object_or_404(Product, id=product_id)
#             cart_items.append({'product': product, 'quantity': qty})

#         return render(request, 'orders/cart.html', {'cart_items': cart_items})

# @method_decorator(customer_required, name='dispatch')
# class CheckoutView(View):
#     def get(self, request):
#         cart = request.session.get('cart', {})
#         cart_items = []
#         for product_id, qty in cart.items():
#             product = get_object_or_404(Product, id=product_id)
#             cart_items.append({'product': product, 'quantity': qty})

#         user_id = request.session.get('user_id')
#         user = get_object_or_404(User, id=user_id) if user_id else None

#         return render(request, 'orders/checkout.html', {
#             'cart_items': cart_items,
#             'user': user  
#         })

#     def post(self, request):
#         cart = request.session.get('cart', {})
#         user_id = request.session.get('user_id')
#         user = get_object_or_404(User, id=user_id)

#         address = request.POST.get('address')
#         phone_no = request.POST.get('phone_no')
#         special_instructions = request.POST.get('special_instructions', '')

#         order = Order.objects.create(
#             user=user,
#             address=address,
#             phone_no=phone_no,
#             special_instructions=special_instructions
#         )

#         for product_id, qty in cart.items():
#             OrderItem.objects.create(
#                 order=order,
#                 product_id=product_id,
#                 quantity=qty
#             )

#         request.session['cart'] = {}
#         return redirect('order_success')
