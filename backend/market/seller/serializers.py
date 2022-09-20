from rest_framework import serializers
from .models import SellerReview


class SellerReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerReview
        fields = "__all__"
