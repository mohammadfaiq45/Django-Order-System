from django.shortcuts import render, redirect, get_object_or_404
from .models import Product

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})


def product_add(request):
    if request.method == 'POST':
        Product.objects.create(
            name=request.POST['name'],
            description=request.POST['description'],
            visibility=request.POST.get('visibility') == 'on',
            available_units=request.POST['available_units']
        )
        return redirect('product_list')
    return render(request, 'products/product_add.html')


def product_edit(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        product.name = request.POST['name']
        product.description = request.POST['description'] 
        product.visibility = request.POST.get('visibility') == 'on'
        product.available_units = request.POST['available_units']
        product.save()
        return redirect('product_list')

    return render(request, 'products/product_edit.html', {'product': product})


def product_delete(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect('product_list')

