from rest_framework import serializers
from .models import Order, OrderItem
from catalog.serializers import ProductImageSerializer, DEFAULT_PRODUCT_IMG


class OrderItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='product.id')
    title = serializers.CharField(source='product.title')
    price = serializers.FloatField()
    count = serializers.IntegerField(source='quantity')
    shortDescription = serializers.CharField(source='product.short_description')
    images = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ('id', 'title', 'price', 'count', 'shortDescription', 'images')

    def get_images(self, obj):
        images = obj.product.images.all()
        if images:
            return [{'src': img.image.url, 'alt': obj.product.title} for img in images]
        return [{'src': DEFAULT_PRODUCT_IMG, 'alt': obj.product.title}]


class OrderSerializer(serializers.ModelSerializer):
    products = OrderItemSerializer(source='items', many=True, read_only=True)
    totalCost = serializers.FloatField(source='total_cost')
    createdAt = serializers.DateTimeField(source='created_at', format="%d.%m.%Y %H:%M")
    fullName = serializers.CharField(source='user.full_name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    phone = serializers.CharField(source='user.phone', read_only=True)

    deliveryType = serializers.CharField(source='delivery_type')
    paymentType = serializers.CharField(source='payment_type')
    paymentError = serializers.CharField(source='payment_error')

    class Meta:
        model = Order
        fields = (
            'id', 'createdAt', 'fullName', 'email', 'phone', 'city', 'address',
            'deliveryType', 'paymentType', 'totalCost', 'status', 'paymentError', 'products'
        )


class OrderPreviewSerializer(serializers.Serializer):
    # Здесь нам не нужны модели, просто отдаем готовые цифры
    totalCost = serializers.FloatField()
    deliveryCost = serializers.FloatField()
    products = serializers.ListField() # Сюда положим товары из корзины
