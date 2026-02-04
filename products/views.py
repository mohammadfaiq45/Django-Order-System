from django.shortcuts import render, redirect, get_object_or_404
from .models import Product

def admin_product_list(request):
    products = Product.objects.all()
    return render(request, 'products/admin_product_list.html', {'products': products})

def customer_product_list(request):
    products = Product.objects.filter(
        visibility=True,
        available_units__gt=0
    )
    return render(request, 'products/customer_product_list.html', {'products': products})

def product_add(request):
    if request.method == 'POST':
        Product.objects.create(
            name=request.POST['name'],
            description=request.POST['description'],
            visibility=request.POST.get('visibility') == 'on',
            available_units=request.POST['available_units']
        )
        return redirect('admin_product_list')
    return render(request, 'products/product_add.html')


def product_edit(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        product.name = request.POST['name']
        product.description = request.POST['description'] 
        product.visibility = request.POST.get('visibility') == 'on'
        product.available_units = request.POST['available_units']
        product.save()
        return redirect('admin_product_list')

    return render(request, 'products/product_edit.html', {'product': product})


def product_delete(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect('admin_product_list')











# from django.shortcuts import render, redirect, get_object_or_404
# from django.views import View
# from django.views.generic import ListView
# from .models import Product


# class AdminProductListView(ListView):
#     model = Product
#     template_name = 'products/admin_product_list.html'
#     context_object_name = 'products'


# class CustomerProductListView(ListView):
#     model = Product
#     template_name = 'products/customer_product_list.html'
#     context_object_name = 'products'

#     def get_queryset(self):
#         return Product.objects.filter(
#             visibility=True,
#             available_units__gt=0
#         )


# class ProductCreateView(View):
#     def get(self, request):
#         return render(request, 'products/product_add.html')

#     def post(self, request):
#         Product.objects.create(
#             name=request.POST['name'],
#             description=request.POST['description'],
#             visibility=request.POST.get('visibility') == 'on',
#             available_units=request.POST['available_units']
#         )
#         return redirect('admin_product_list')


# class ProductUpdateView(View):
#     def get(self, request, id):
#         product = get_object_or_404(Product, id=id)
#         return render(request, 'products/product_edit.html', {'product': product})

#     def post(self, request, id):
#         product = get_object_or_404(Product, id=id)
#         product.name = request.POST['name']








