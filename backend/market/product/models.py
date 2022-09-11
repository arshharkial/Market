from django.db import models
from django.contrib.auth import get_user_model
from brand.models import Brand
from django.contrib.postgres.fields import ArrayField

User = get_user_model()
PRODUCT_CATEGORIES = []


class Product(models.Model):
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="my_products"
    )
    category = models.CharField(
        max_length=100, blank=False, null=False, choices=PRODUCT_CATEGORIES
    )
    name = models.CharField(max_length=100, blank=False, null=False)
    brand_name = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name="my_brand_products"
    )
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=False, null=False
    )
    images = ArrayField(
        models.CharField(
            null=True,
            blank=True,
            max_length=256,
        ),
        blank=True,
        default=list,
        null=True,
    )
    videos = ArrayField(
        models.CharField(
            null=True,
            blank=True,
            max_length=256,
        ),
        blank=True,
        default=list,
        null=True,
    )


class Reviews(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="my_reviews"
    )
    title = models.CharField(max_length=300, blank=False, null=False)
    description = models.TextField()
    reviewer = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="my_reviews"
    )
    rating = models.DecimalField(
        max_digits=3, decimal_places=2, blank=False, null=False
    )
    images = ArrayField(
        models.CharField(
            null=True,
            blank=True,
            max_length=256,
        ),
        blank=True,
        default=list,
        null=True,
    )
    videos = ArrayField(
        models.CharField(
            null=True,
            blank=True,
            max_length=256,
        ),
        blank=True,
        default=list,
        null=True,
    )
