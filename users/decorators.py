from functools import wraps
from django.shortcuts import redirect


def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('login')

        if not request.session.get('is_admin'):
            return redirect('customer_product_list')

        return view_func(request, *args, **kwargs)
    return wrapper


def customer_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('login')

        if request.session.get('is_admin'):
            return redirect('admin_product_list')

        return view_func(request, *args, **kwargs)
    return wrapper

