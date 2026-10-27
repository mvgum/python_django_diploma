from celery import shared_task
from .models import Order
import time
import random


@shared_task
def process_payment(order_id, card_number):
    # Имитация задержки ответа от платежной системы
    time.sleep(3)

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return

    # Логика из ТЗ:
    # Если номер четный и не заканчивается на 0 — успех
    is_even = int(card_number) % 2 == 0
    ends_with_zero = str(card_number).endswith('0')

    if is_even and not ends_with_zero:
        order.status = 'paid'
        order.payment_error = None
    else:
        order.status = 'error'
        order.payment_error = 'Ошибка оплаты: неверный номер карты или недостаточно средств.'

    order.save()
