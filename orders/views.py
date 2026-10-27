from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.db import transaction
from .models import Order, OrderItem, ShopSettings
from .serializers import OrderSerializer
from cart.models import CartItem
from cart.views import get_cart
from .tasks import process_payment # <--- Импорт задачи


class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = get_cart(request)
        cart_items = CartItem.objects.filter(cart=cart)

        if not cart_items:
            return Response({'error': 'Корзина пуста'}, status=400)

        # --- ХИТРОСТЬ: Если пришел список, значит фронтенд шлет товары ---
        if isinstance(request.data, list):
            # Берем данные из последнего шага (предполагаем, что они есть в сессии или ставим дефолт)
            # К сожалению, фронтенд Skillbox не передает город и адрес в этом запросе,
            # поэтому мы подставим заглушки, чтобы заказ создался.
            data = {
                'city': 'Москва',
                'address': 'ул. Пушкина, д. 1',
                'deliveryType': 'standard',
                'paymentType': 'online'
            }
        else:
            # Если пришел словарь, берем данные оттуда
            data = request.data

        # Считаем сумму товаров
        total_cost = sum(item.product.price * item.quantity for item in cart_items)

        # Рассчитываем доставку
        settings_obj, _ = ShopSettings.objects.get_or_create(id=1)
        delivery_cost = 0
        delivery_type = data.get('deliveryType', 'standard')

        if delivery_type == 'express':
            delivery_cost = settings_obj.express_delivery_cost
        else:
            if total_cost < settings_obj.free_delivery_threshold:
                delivery_cost = settings_obj.standard_delivery_cost

        final_cost = total_cost + delivery_cost

        # Создаем заказ
        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                city=data.get('city', ''),
                address=data.get('address', ''),
                delivery_type=delivery_type,
                payment_type=data.get('paymentType', 'online'),
                total_cost=final_cost,
                status='pending'
            )

            # Переносим товары
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

            # Очищаем корзину
            cart_items.delete()

        return Response({'orderId': order.id}, status=201)

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, is_deleted=False).order_by('-created_at')


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, is_deleted=False)


class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            order = Order.objects.get(id=pk, user=request.user)
        except Order.DoesNotExist:
            return Response({'error': 'Заказ не найден'}, status=404)

        card_number = request.data.get('number')
        if not card_number or not card_number.isdigit():
            return Response({'error': 'Неверный формат номера'}, status=400)

        # Меняем способ оплаты, если пользователь выбрал другой на странице оплаты
        payment_type = request.data.get('paymentType')
        if payment_type:
            order.payment_type = payment_type
            order.save()

        # Запускаем задачу в Celery
        from .tasks import process_payment
        process_payment.delay(order.id, str(card_number))

        return Response({'message': 'Ждём подтверждения оплаты от платёжной системы'}, status=200)


class OrderPreviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = get_cart(request)
        cart_items = CartItem.objects.filter(cart=cart)

        from cart.serializers import CartItemSerializer
        products_data = CartItemSerializer(cart_items, many=True).data

        total_products_cost = sum(item.product.price * item.quantity for item in cart_items)

        # Получаем настройки доставки
        settings_obj, _ = ShopSettings.objects.get_or_create(id=1)

        # По умолчанию считаем обычную доставку
        delivery_cost = 0
        if total_products_cost < settings_obj.free_delivery_threshold:
            delivery_cost = settings_obj.standard_delivery_cost

        final_cost = total_products_cost + delivery_cost

        return Response({
            'totalCost': final_cost,
            'deliveryCost': delivery_cost,
            'products': products_data
        })
