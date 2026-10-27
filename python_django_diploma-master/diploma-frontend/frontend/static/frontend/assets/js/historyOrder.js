var mix = {
	methods: {
		getOrders() {
			// ИСПРАВЛЕНО: запрашиваем список по адресу /api/orders/list/
			this.getData('/api/orders/list/')
				.then(data => {
					this.orders = data.map(order => ({
						id: order.id,
						createdAt: order.createdAt,
						deliveryType: order.deliveryType === 'express' ? 'Экспресс-доставка' : 'Обычная доставка',
						paymentType: order.paymentType === 'online' ? 'Онлайн картой' : 'Онлайн со случайного счета',
						totalCost: order.totalCost,
						status: order.status === 'paid' ? 'Оплачен' : (order.status === 'pending' ? 'Ожидает оплаты' : 'Ошибка оплаты')
					}));
				})
				.catch(err => console.error("Ошибка загрузки истории заказов:", err));
		}
	},
	mounted() {
		this.getOrders();
	},
	data() {
		return {
			orders: []
		}
	}
}