from django.db import models
from category.models import Category
from nike_shop import settings

User = settings.AUTH_USER_MODEL


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='images', null=True, blank=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f'{self.title} - - - Цена: {self.price} сом'


class Like(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked')

    class Meta:
        unique_together = ['product', 'owner']


class Favourites(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favourites')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourites')

    class Meta:
        unique_together = ['product', 'user']



