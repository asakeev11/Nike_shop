from rest_framework import serializers
from .models import Product, Like, Favourites
from django.db.models import Avg


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('title', 'price', 'image')


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    
    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['raiting'] = instance.reviews.aggregate(Avg('raiting'))['raiting__avg']
        repr['reviews'] = instance.reviews.count()
        return repr


    def is_liked(self, product):
        user = self.context.get('request').user
        return user.liked.filter(product=product).exists()

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        user = self.context.get('request').user
        if user.is_authenticated:
            repr['is_liked'] = self.is_liked(instance)
        repr['likes_count'] = instance.likes.count()
        return repr


# LIKES
class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Like
        fields = ('owner',)


# FAVOURITES
class FavouritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourites
        fields = ('product',)

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['product'] = ProductListSerializer(instance.product).data
        return repr
