from django.db import models

class Product(models.Model):
    code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=100, unique=True)
    price = models.BigIntegerField()
    status = models.BooleanField(default=True)

class Sale(models.Model):
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    slug = models.TextField(unique=True)
    buyer_name = models.CharField(max_length=20)
    buyer_phone = models.CharField(max_length=15)
    buyer_address = models.CharField(max_length=200)
    ongkir = models.BigIntegerField(default=0)
    sale_date = models.DateField()
    created_at = models.DateTimeField()
    status = models.BooleanField(default=True)

class SaleProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    sale = models.ForeignKey(Sale, on_delete=models.PROTECT)
    amount = models.IntegerField(default=0)
    price = models.BigIntegerField(default=0)