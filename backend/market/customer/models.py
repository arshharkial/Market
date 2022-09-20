from django.db import models
from backend.market.product.models import Product
from backend.market.user.models import Address

# Create your models here.


class Cart(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)
    total = models.DecimalField(
        max_digits=100, decimal_places=2, blank=False, null=False
    )


class CartItem(models.Model):
    item = models.ForeignKey(Product, on_delete=models.PROTECT, blank=False, null=False)
    quantity = models.IntegerField(blank=None, null=None, default=1)
    price = models.DecimalField(max_digits=100, decimal_places=2, blank=False, null=False)
    cart = models.ForeignKey(Cart, on_delete=models.)


class Wishlist(models.Model):
    name = models.CharField(max_length=50, blank=None, null=None)
    visibile = models.BooleanField(blank=False, null=False, default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(
        Wishlist, on_delete=models.CASCADE, related_name="wishlist_items", blank=False, null=False
    )
    item = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False, null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)


class Order(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)
    total = models.DecimalField(
        max_digits=100, decimal_places=2, blank=False, null=False
    )
    address = models.ForeignKey(Address, blank=False, null=False, on_delete=models.PROTECT)


class OrderItem(models.Model):
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, blank=False, null=False)
    quantity = models.IntegerField(default=1, blank=False, null=False)
    price = models.DecimalField(
        max_digits=100, decimal_places=2, blank=False, null=False
    )
    date_created = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)
