from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from . import serializers
from .models import Product, Like, Favourites


# PAGINATION
class StandartResultsPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'page'
    max_page_size = 1000


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandartResultsPagination
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('category',)
    search_fields = ('title',)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ProductListSerializer
        return serializers.ProductDetailSerializer

    def get_permissions(self):
        # Лайкать , добавлять в избранное может аутентифицированный юзер
        if self.action in ('like', 'unlike', 'favourite'):
            return [permissions.IsAuthenticated()]
        # Изменять, создавать и удалять может только админ
        elif self.action in ('update', 'partial_update', 'destroy', 'create', 'get_likes'):
            return [permissions.IsAdminUser()]
        # Просматривать могут все
        else:
            return [permissions.AllowAny(), ]

    # Добавление лайка
    @action(['POST'], detail=True)
    def like(self, request, pk):
        product = self.get_object()
        if request.user.liked.filter(product=product).exists():
            return Response('You have already liked  this product', status=400)
        Like.objects.create(product=product, owner=request.user)
        return Response('You liked', status=201)

    # UNLIKE
    @action(['POST'], detail=True)
    def unlike(self, request, pk):
        product = self.get_object()
        if not request.user.liked.filter(product=product).exists():
            return Response('You have not liked this product yet', status=400)
        request.user.liked.filter(product=product).delete()
        return Response('You unliked this product', status=204)

    # Список лайкнувших юзеров может посмотреть только админ
    @action(['GET'], detail=True)
    def get_likes(self, request, pk):
        product = self.get_object()
        likes = product.likes.all()
        serializer = serializers.LikeSerializer(likes, many=True)
        return Response(serializer.data, status=200)

    # Добавление в избранное
    @action(['POST'], detail=True)
    def favourite(self, request, pk):
        product = self.get_object()
        if request.user.favourites.filter(product=product).exists():
            request.user.favourites.filter(product=product).delete()
            return Response('Removed from favourites', status=204)
        Favourites.objects.create(product=product, user=request.user)
        return Response('Added to Favourites', status=201)
