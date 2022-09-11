from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField()
    logo = models.URLField(blank=True, null=False, max_length=255)
