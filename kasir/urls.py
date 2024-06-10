from django.urls import path

from . import views

app_name='kasir'

urlpatterns = [
    path('kasir/', views.index, name='index'),
    path('kasir/products/', views.get_products, name='products'),
    path('kasir/products/create/', views.create_product, name='products.create'),
    path('kasir/products/<int:product_id>/edit/', views.edit_product, name='products.edit'),

    path('kasir/sales/', views.get_sales, name='sales'),
    path('kasir/sales/create/', views.create_sale, name='sales.create'),
    path('kasir/sales/<int:sale_id>/edit/', views.edit_sale, name='sales.edit'),
    path('kasir/sales/<int:sale_id>/add-product/', views.add_product_sale, name='sales.add_product'),
    path('kasir/sales/<int:sale_id>/delete/', views.delete_sale, name='sales.delete'),
    path('kasir/sales/<int:sale_id>/print-receipt', views.sale_receipt_print, name='sales.receipt.print'),
]