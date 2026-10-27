from django.db import models
from django.conf import settings
from catalog.models import Product

class ShopSettings(models.Model):
    """Настройки магазина (задаются в админке)"""
    express_delivery_cost = models.DecimalField(max_digits=10, decimal_places=2, default=500, verbose_name="Стоимость экспресс-доставки")
    free_delivery_threshold = models.DecimalField(max_digits=10, decimal_places=2, default=2000, verbose_name="Порог бесплатной доставки")
    standard_delivery_cost = models.DecimalField(max_digits=10, decimal_places=2, default=200, verbose_name="Стоимость обычной доставки")

    class Meta:
        verbose_name = "Настройки магазина"
        verbose_name_plural = "Настройки магазина"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('paid', 'Оплачен'),
        ('error', 'Ошибка оплаты'),
    ]
    DELIVERY_CHOICES = [
        ('standard', 'Обычная доставка'),
        ('express', 'Экспресс-доставка'),
    ]
    PAYMENT_CHOICES = [
        ('online', 'Онлайн картой'),
        ('someone', 'Онлайн со случайного чужого счета'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    delivery_type = models.CharField(max_length=20, choices=DELIVERY_CHOICES, default='standard')
    payment_type = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='online')

    city = models.CharField(max_length=100)
    address = models.TextField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    payment_error = models.TextField(null=True, blank=True, verbose_name="Текст ошибки оплаты")
    is_deleted = models.BooleanField(default=False) # Мягкое удаление

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2) # Фиксируем цену на момент покупки

class ShopSettings(models.Model):
    express_delivery_cost = models.DecimalField(max_digits=10, decimal_places=2, default=500, verbose_name="Стоимость экспресс-доставки")
    free_delivery_threshold = models.DecimalField(max_digits=10, decimal_places=2, default=2000, verbose_name="Порог бесплатной доставки")
    standard_delivery_cost = models.DecimalField(max_digits=10, decimal_places=2, default=200, verbose_name="Стоимость обычной доставки")

    class Meta:
        verbose_name = "Настройки магазина"
        verbose_name_plural = "Настройки магазина"
