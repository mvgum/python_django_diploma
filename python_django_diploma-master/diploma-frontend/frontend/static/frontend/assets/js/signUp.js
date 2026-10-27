var mix = {
	methods: {
		signUp () {
			const nameEl = document.querySelector('#name');
			const name = nameEl ? nameEl.value : '';
			const username = document.querySelector('#login').value;
			const password = document.querySelector('#password').value;

			// Передаем объект { name, username, password }
			this.postData('/api/sign-up/', { name, username, password })
				.then(({ data, status }) => {
					location.assign(`/`)
				})
				.catch((error) => {
					console.error("Ошибка регистрации:", error);
					alert("Ошибка регистрации. Проверьте данные.");
				})
		}
	},
	data() {
		return {}
	}
}