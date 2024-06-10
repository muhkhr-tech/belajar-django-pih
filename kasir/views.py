from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from django.contrib import messages
from django.utils.text import slugify
from django.utils.crypto import get_random_string

from datetime import datetime

def index(request):
    return render(request, 'kasir/index.html')

from .models import *

def get_products(request):
    data = Product.objects.all()

    context = {
        'data': data
    }

    return render(request, 'kasir/product.html', context=context)

def create_product(request):
    if request.method == 'POST':
        new_product = Product()
        new_product.code = get_random_string(5)
        new_product.slug = slugify(request.POST['product_name']+request.POST['product_price'])
        new_product.name = request.POST['product_name']
        new_product.price = request.POST['product_price']
        new_product.save()

        return redirect('kasir:products')
    
    return render(request, 'kasir/product-create.html')

def edit_product(request, product_id):

    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        
        product.slug = slugify(request.POST['product_name']+request.POST['product_price'])
        product.name = request.POST['product_name']
        product.price = request.POST['product_price']
        product.save()

        return redirect('kasir:products')
    
    context = {
        'product': product
    }
    
    return render(request, 'kasir/product-edit.html', context=context)


def get_sales(request):
    data = Sale.objects.filter(status=True).all()

    context = {
        'data': data
    }

    return render(request, 'kasir/sale.html', context=context)

def create_sale(request):

    products = Product.objects.all()

    product = Product.objects.filter(pk=request.GET.get('product_id')).first()

    if request.method == 'POST':

        new_sale = Sale()
        new_sale.code = get_random_string(5)
        new_sale.slug = slugify(request.POST['sale_buyer_name']+request.POST['sale_buyer_phone']+request.POST['sale_buyer_address']+request.POST['sale_date'])
        new_sale.description = request.POST['sale_description']
        new_sale.buyer_name = request.POST['sale_buyer_name']
        new_sale.buyer_phone = request.POST['sale_buyer_phone']
        new_sale.buyer_address = request.POST['sale_buyer_address']
        new_sale.sale_date = request.POST['sale_date']
        new_sale.ongkir = request.POST['sale_ongkir']
        new_sale.created_at = datetime.now()
        new_sale.save()

        for idx in range(0, len(request.POST.getlist('product'))):
            SaleProduct.objects.create(
                product_id=request.POST.getlist('product')[idx],
                sale_id=new_sale.id,
                amount=request.POST.getlist('amount')[idx],
                price=request.POST.getlist('price')[idx]
            )

        return HttpResponseRedirect(reverse("kasir:sales.add_product", kwargs={"sale_id": new_sale.id}))
    
    context = {
        'products': products,
        'product': product,
    }
    
    return render(request, 'kasir/sale-create.html', context=context)

def edit_sale(request, sale_id):

    sale = get_object_or_404(Sale, pk=sale_id)

    if request.method == 'POST':

        sale.slug = slugify(request.POST['sale_buyer_name']+request.POST['sale_buyer_phone']+request.POST['sale_buyer_address']+request.POST['sale_date'])
        sale.description = request.POST['sale_description']
        sale.buyer_name = request.POST['sale_buyer_name']
        sale.buyer_phone = request.POST['sale_buyer_phone']
        sale.buyer_address = request.POST['sale_buyer_address']
        sale.sale_date = request.POST['sale_date']
        sale.ongkir = request.POST['sale_ongkir']
        sale.save()

        return redirect('kasir:sales')
    
    context = {
        'sale': sale
    }
    
    return render(request, 'kasir/sale-edit.html', context=context)

def sale_receipt(request, sale_id):

    sale = get_object_or_404(Sale, pk=sale_id)
    data = SaleProduct.objects.filter(sale=sale).all()
    
    context = {
        'sale': sale,
        'data': data
    }
    
    return render(request, 'kasir/sale-receipt.html', context=context)

def sale_receipt_print(request, sale_id):

    sale = get_object_or_404(Sale, pk=sale_id)
    data = SaleProduct.objects.filter(sale=sale).all()
    
    context = {
        'sale': sale,
        'data': data
    }
    
    return render(request, 'kasir/sale-receipt.html', context=context)

def add_product_sale(request, sale_id):

    products = Product.objects.all()

    product = Product.objects.filter(pk=request.GET.get('product_id')).first()

    sale = get_object_or_404(Sale, pk=sale_id)

    sale_products = SaleProduct.objects.filter(
        sale=sale
    ).all()

    if request.method == 'POST':
        
        sale_product = SaleProduct.objects.filter(
            sale=sale,
            product=product
        ).first()

        if sale_product:
            sale_product.amount = request.POST['sale_product_amount']
            sale_product.price = request.POST['sale_product_price']
            sale_product.save()
        else:
            new_sale_product = SaleProduct()
            new_sale_product.sale = sale
            new_sale_product.product = product
            new_sale_product.amount = request.POST['sale_product_amount']
            new_sale_product.price = request.POST['sale_product_price']
            new_sale_product.save()

        return HttpResponseRedirect(reverse("kasir:sales.add_product", kwargs={"sale_id": sale.id}))
    
    context = {
        'sale': sale,
        'sale_products': sale_products,
        'products': products,
        'product': product,
    }
    
    return render(request, 'kasir/sale-add-product.html', context=context)

def delete_sale(request, sale_id):

    sale = get_object_or_404(Sale, pk=sale_id)

    if request.method == 'POST':
        
        sale.status = False
        sale.save()

        return HttpResponseRedirect(reverse("kasir:sales"))
    
    return HttpResponseNotFound()