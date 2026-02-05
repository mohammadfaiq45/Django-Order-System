from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from .models import Product
from django.utils.decorators import method_decorator
from users.decorators import admin_required, customer_required

@method_decorator(admin_required, name='dispatch')
class AdminProductListView(ListView):
    model = Product
    template_name = 'products/admin_product_list.html'
    context_object_name = 'products'

# @method_decorator(customer_required, name='dispatch')
class CustomerProductListView(ListView):
    model = Product
    template_name = 'products/customer_product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(
            visibility=True,
            available_units__gt=0
        )


@method_decorator(admin_required, name='dispatch')
class ProductCreateView(View):
    def get(self, request):
        return render(request, 'products/product_add.html')

    def post(self, request):
        Product.objects.create(
            name=request.POST['name'],
            description=request.POST['description'],
            visibility=request.POST.get('visibility') == 'on',
            available_units=request.POST['available_units']
        )
        return redirect('admin_product_list')

@method_decorator(admin_required, name='dispatch')
class ProductUpdateView(View):
    def get(self, request, id):
        product = get_object_or_404(Product, id=id)
        return render(request, 'products/product_edit.html', {'product': product})

    def post(self, request, id):
        product = get_object_or_404(Product, id=id)
        product.name = request.POST['name']
        product.description = request.POST['description']
        product.visibility = request.POST.get('visibility') == 'on'
        product.available_units = request.POST['available_units']
        product.save()
        return redirect('admin_product_list')

@method_decorator(admin_required, name='dispatch')
class ProductDeleteView(View):
    def get(self, request, id):
        product = get_object_or_404(Product, id=id)
        product.delete()
        return redirect('admin_product_list')
