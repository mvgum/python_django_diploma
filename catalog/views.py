from rest_framework import generics
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Count
from rest_framework.views import APIView

from .models import Product, Category, Specification, ProductSpecification, Banner
from .serializers import ProductSerializer, CategorySerializer, BannerSerializer


class CatalogFiltersView(APIView):
    def get(self, request, category_id):
        specs = Specification.objects.filter(category_id=category_id)

        # Формируем список фильтров для фронтенда
        filters_data = []
        for spec in specs:
            # Получаем уникальные значения для этой характеристики среди товаров
            values = ProductSpecification.objects.filter(
                specification=spec,
                product__is_deleted=False
            ).values_list('value', flat=True).distinct()

            filters_data.append({
                'id': spec.id,
                'name': spec.name,
                'type': spec.filter_type,  # 'choice', 'checkbox', 'text'
                'values': list(values)
            })

        return Response(filters_data)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.filter(parent__isnull=True, is_deleted=False)
    serializer_class = CategorySerializer
    pagination_class = None  # <--- Отключаем пагинацию, фронтенд ждет массив


class CatalogPagination(PageNumberPagination):
    page_size = 20 # Фронтенд просит limit=20
    page_size_query_param = 'limit'

class CatalogListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = CatalogPagination

    def get_queryset(self):
        queryset = Product.objects.filter(is_deleted=False).annotate(reviews_count=Count('reviews'))

        # 1. Фильтр по названию (фронтенд шлет filter[name])
        title = self.request.query_params.get('filter[name]') or self.request.query_params.get('title')
        if title:
            queryset = queryset.filter(title__icontains=title)

        # 2. Фильтр по цене (фронтенд шлет filter[minPrice] и filter[maxPrice])
        min_price = self.request.query_params.get('filter[minPrice]')
        max_price = self.request.query_params.get('filter[maxPrice]')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        # 3. Фильтр по категории (из URL, например /api/catalog/?category=1)
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category__in=Category.objects.filter(Q(id=category_id) | Q(parent_id=category_id)))

        # 4. Сортировка
        sort_by = self.request.query_params.get('sort', 'popular')
        sort_type = self.request.query_params.get('sortType', 'dec') # 'inc' или 'dec'
        prefix = '' if sort_type == 'inc' else '-'

        if sort_by == 'price':
            queryset = queryset.order_by(f'{prefix}price')
        elif sort_by == 'reviews':
            queryset = queryset.order_by(f'{prefix}reviews_count')
        elif sort_by == 'date':
            queryset = queryset.order_by(f'{prefix}id')
        elif sort_by == 'rating': # Популярность
            queryset = queryset.order_by(f'{prefix}sort_index', f'{prefix}purchases_count')
        else:
            queryset = queryset.order_by('-sort_index', '-purchases_count')

        return queryset


class PopularProductsView(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = None  # <--- Отключаем пагинацию

    def get_queryset(self):
        return Product.objects.filter(is_deleted=False).order_by('-sort_index', '-purchases_count')[:8]


class LimitedProductsView(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = None  # <--- Отключаем пагинацию

    def get_queryset(self):
        return Product.objects.filter(is_deleted=False, limited_edition=True)[:16]


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_deleted=False)
    serializer_class = ProductSerializer


class BannerListView(generics.ListAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    pagination_class = None  # <--- Отключаем пагинацию


class TagListView(APIView):
    def get(self, request):
        # Возвращаем пустой список, чтобы фронтенд не падал
        return Response([])
