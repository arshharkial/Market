from rest_framework import serializers
from .models import Brand, BrandReviews


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class BrandReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandReviews
        fields = "__all__"
