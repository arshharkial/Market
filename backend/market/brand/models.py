from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField

User = get_user_model()


class Brand(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField()
    logo = models.URLField(blank=True, null=False, max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)


class BrandReviews(models.Model):
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name="my_recieved_reviews"
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
    date_created = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)
