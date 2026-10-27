from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Cart, CartItem
from catalog.models import Product
from .serializers import CartItemSerializer


def get_cart(request):
    """Вспомогательная функция: получает корзину пользователя или создает новую (для гостей по сессии)"""
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


class BasketView(APIView):
    def get(self, request):
        """Получить все товары в корзине"""
        cart = get_cart(request)
        items = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Добавить товар в корзину"""
        cart = get_cart(request)
        product_id = request.data.get('id')
        count = int(request.data.get('count', 1))

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Товар не найден'}, status=404)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if created:
            cart_item.quantity = count
        else:
            cart_item.quantity += count
        cart_item.save()

        # Возвращаем обновленный список корзины
        items = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data)

    def delete(self, request):
        cart = get_cart(request)
        product_id = request.data.get('id')
        count = int(request.data.get('count', 1))

        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            if cart_item.quantity > count:
                cart_item.quantity -= count
                cart_item.save()
            else:
                cart_item.delete()
        except CartItem.DoesNotExist:
            pass

        items = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data)
