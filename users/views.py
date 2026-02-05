from django.shortcuts import render, redirect
from .models import User

def login_view(request):
    error = None

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                request.session['user_id'] = user.id
                request.session['is_admin'] = user.is_admin

                if user.is_admin:
                    return redirect('admin_product_list')   
                else:
                    return redirect('customer_product_list')
            else:
                error = 'Invalid password'
        except User.DoesNotExist:
            error = 'User not found'

    return render(request, 'users/login.html', {'error': error})


def logout_view(request):
    request.session.flush()
    return redirect('login')
