from django.contrib import admin
from .models import Order, OrderItem, ShopSettings

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('price',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'status', 'total_cost', 'is_deleted')
    list_filter = ('status', 'is_deleted')
    inlines = [OrderItemInline]

@admin.register(ShopSettings)
class ShopSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Разрешаем создавать только одну запись настроек
        return not ShopSettings.objects.exists()
