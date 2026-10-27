from rest_framework import serializers
from .models import Category, Product, ProductImage, Review, Banner, ProductSpecification


# Заглушки для картинок
DEFAULT_CATEGORY_IMG = '/static/frontend/assets/img/icons/departments/1.svg'
DEFAULT_PRODUCT_IMG = '/static/frontend/assets/img/content/home/card.jpg'


class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'image', 'subcategories')

    def get_image(self, obj):
        if obj.image:
            return {'src': obj.image.url, 'alt': obj.name}
        return {'src': DEFAULT_CATEGORY_IMG, 'alt': obj.name}  # Заглушка

    def get_subcategories(self, obj):
        subcats = obj.subcategories.filter(is_deleted=False)
        return [{
            'id': sub.id,
            'title': sub.name,
            'image': {'src': sub.image.url if sub.image else DEFAULT_CATEGORY_IMG, 'alt': sub.name}
        } for sub in subcats]


class ProductImageSerializer(serializers.ModelSerializer):
    src = serializers.ImageField(source='image')
    alt = serializers.CharField(source='product.title')

    class Meta:
        model = ProductImage
        fields = ('src', 'alt')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='user.full_name', read_only=True)
    date = serializers.DateTimeField(source='created_at', format="%Y-%m-%d %H:%M")

    class Meta:
        model = Review
        fields = ('id', 'author', 'text', 'rating', 'date')


class ProductSpecificationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='specification.name')
    value = serializers.CharField()

    class Meta:
        model = ProductSpecification
        fields = ('name', 'value')


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()  # Изменили на MethodField
    price = serializers.FloatField()
    reviews = ReviewSerializer(many=True, read_only=True)
    fullDescription = serializers.CharField(source='description')
    specifications = ProductSpecificationSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'title', 'short_description', 'description', 'price', 'images', 'reviews', 'fullDescription',
                  'specifications')

    def get_images(self, obj):
        images = obj.images.all()
        if images:
            return ProductImageSerializer(images, many=True).data
        return [{'src': DEFAULT_PRODUCT_IMG, 'alt': obj.title}]  # Заглушка, если нет фото


class BannerSerializer(serializers.ModelSerializer):
    category = serializers.IntegerField(source='category.id')
    images = serializers.SerializerMethodField()

    class Meta:
        model = Banner
        fields = ('id', 'title', 'category', 'price', 'images')

    def get_images(self, obj):
        if obj.image:
            return [{'src': obj.image.url, 'alt': obj.title}]
        return [{'src': DEFAULT_PRODUCT_IMG, 'alt': obj.title}]
