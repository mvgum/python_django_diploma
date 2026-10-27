var mix = {
	methods: {
		loadOrder() {
			// Получаем ID заказа из URL (например, /orders/10/ -> 10)
			const urlParts = window.location.pathname.split('/');
			const orderId = urlParts[urlParts.length - 2];

			this.getData(`/api/order/${orderId}/`)
				.then(data => {
					this.orderId = data.id;
					this.createdAt = data.createdAt;
					this.fullName = data.fullName;
					this.phone = data.phone;
					this.email = data.email;
					this.deliveryType = data.deliveryType === 'express' ? 'Экспресс-доставка' : 'Обычная доставка';
					this.paymentType = data.paymentType === 'online' ? 'Онлайн картой' : 'Онлайн со случайного счета';
					this.city = data.city;
					this.address = data.address;
					this.status = data.status === 'paid' ? 'Оплачен' : (data.status === 'pending' ? 'Ожидает оплаты' : 'Ошибка оплаты');
					this.totalCost = data.totalCost;
					this.products = data.products;
					this.paymentError = data.paymentError;
				})
				.catch(err => console.error("Ошибка загрузки заказа:", err));
		},
		loadPreview() {
			// (Эта функция для страницы оформления, можно оставить)
			this.getData('/api/orders/preview/')
				.then(data => {
					this.orderPreview = data;
					this.products = data.products;
				})
				.catch(err => console.error("Ошибка загрузки предпросмотра:", err));
		},
		confirmOrder() {
			// (Эта функция для страницы оформления, можно оставить)
			const cityInput = document.querySelector('#city');
			const addressInput = document.querySelector('#address');
			const payload = {
				city: cityInput ? cityInput.value : 'Москва',
				address: addressInput ? addressInput.value : 'Не указан',
				deliveryType: this.deliveryType || 'standard',
				paymentType: this.paymentType || 'online'
			};
			this.postData('/api/orders/', payload)
				.then(({ data }) => {
					if (data.orderId) {
						location.assign(`/payment/${data.orderId}/`);
					}
				})
				.catch(err => console.error("Ошибка создания заказа:", err));
		}
	},
	mounted() {
		// Если мы на странице оформления заказа, грузим предпросмотр
		if (window.location.pathname === '/orders/') {
			this.loadPreview();
		}
		// Если мы на странице детального просмотра заказа, грузим сам заказ
		if (window.location.pathname.includes('/orders/') && window.location.pathname !== '/orders/') {
			this.loadOrder();
		}
	},
	data() {
		return {
			orderPreview: { totalCost: 0 },
			products: [],
			orderId: null,
			createdAt: '',
			fullName: '',
			phone: '',
			email: '',
			city: '',
			address: '',
			deliveryType: '',
			paymentType: '',
			status: '',
			totalCost: 0,
			paymentError: null
		}
	}
}