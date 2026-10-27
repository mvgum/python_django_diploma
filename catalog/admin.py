from django.contrib import admin
from .models import Category, Product, ProductImage, Specification, ProductSpecification, Review, Banner

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'is_deleted')
    list_filter = ('is_deleted',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'sort_index', 'limited_edition', 'is_deleted')
    list_filter = ('category', 'limited_edition', 'is_deleted')
    search_fields = ('title',)
    inlines = [ProductImageInline, ProductSpecificationInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price')

