from rest_framework import serializers

from .models import Category
from product.serializers import ProductListSerializer


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['products'] = ProductListSerializer(instance.products.all(), many=True).data
        return representation
