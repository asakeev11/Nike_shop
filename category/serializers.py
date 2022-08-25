from rest_framework import serializers

from .models import Category


class CategoryListSerializer(serializers.ModelSerializer):
    # slug = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = ('name',)


class CategoryDetailSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
