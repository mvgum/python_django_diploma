from django.db import models
from django.conf import settings


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False, verbose_name="Удален")

    objects = SoftDeleteManager()
    all_objects = models.Manager()  # Чтобы видеть всё, включая удаленное

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    def hard_delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)


class Category(SoftDeleteModel):
    name = models.CharField(max_length=255, verbose_name="Название")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    image = models.ImageField(upload_to='categories/', null=True, blank=True, verbose_name="Иконка")

    def __str__(self):
        return self.name


class Product(SoftDeleteModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=255, verbose_name="Название")
    short_description = models.TextField(verbose_name="Краткое описание")
    description = models.TextField(verbose_name="Полное описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")

    # Для сортировки и главной страницы
    sort_index = models.IntegerField(default=0, verbose_name="Индекс сортировки")
    purchases_count = models.IntegerField(default=0, verbose_name="Количество покупок")
    limited_edition = models.BooleanField(default=False, verbose_name="Ограниченный тираж")

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/', verbose_name="Изображение")
    is_main = models.BooleanField(default=False)


class Specification(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название характеристики")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='specifications')
    # Тип фильтра: выбор (dropdown), чекбокс (checkbox), текст (text)
    filter_type = models.CharField(max_length=20,
                                   choices=[('choice', 'Выбор'), ('checkbox', 'Чекбокс'), ('text', 'Текст')])


class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')
    specification = models.ForeignKey(Specification, on_delete=models.CASCADE)
    value = models.CharField(max_length=255, verbose_name="Значение")


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Текст отзыва")
    rating = models.PositiveSmallIntegerField(verbose_name="Оценка", choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)


class Banner(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='banners/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
