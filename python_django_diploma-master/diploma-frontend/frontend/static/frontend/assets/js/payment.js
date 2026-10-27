var mix = {
	methods: {
		submitPayment() {
			// Получаем ID заказа из URL (например, /payment/5/ -> 5)
			const urlParts = window.location.pathname.split('/');
			const orderId = urlParts[urlParts.length - 2];

			// Собираем номер карты из полей (убираем пробелы)
			const cardNumber = document.querySelector('#numero1').value.replace(/\s/g, '');

			const payload = {
				number: cardNumber,
				paymentType: 'online' // По умолчанию онлайн картой
			};

			this.postData(`/api/payment/${orderId}/`, payload)
			    .then(({ data }) => {
			            alert(data.message);
			            // Переходим на страницу ожидания, передавая ID заказа в URL
			            location.assign(`/progress-payment/?orderId=${orderId}`);
			    })
				.catch(err => {
					console.error("Ошибка оплаты:", err);
					alert("Ошибка оплаты. Проверьте номер карты.");
				});
		}
	},
	data() {
		return {}
	}
}