from rest_framework import serializers
from .models import CartItem
from catalog.serializers import DEFAULT_PRODUCT_IMG # Импортируем нашу заглушку

class CartItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='product.id')
    title = serializers.CharField(source='product.title')
    price = serializers.FloatField(source='product.price')
    images = serializers.SerializerMethodField() # Меняем на метод
    count = serializers.IntegerField(source='quantity')
    shortDescription = serializers.CharField(source='product.short_description')

    class Meta:
        model = CartItem
        fields = ('id', 'title', 'price', 'images', 'count', 'shortDescription')

    def get_images(self, obj):
        # Если у товара есть картинки, отдаем их
        images = obj.product.images.all()
        if images:
            return [{'src': img.image.url, 'alt': obj.product.title} for img in images]
        # Если картинок нет — отдаем заглушку
        return [{'src': DEFAULT_PRODUCT_IMG, 'alt': obj.product.title}]
