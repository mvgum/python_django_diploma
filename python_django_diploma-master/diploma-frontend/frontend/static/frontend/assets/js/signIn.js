var mix = {
	methods: {
		signIn () {
			const username = document.querySelector('#login').value;
			const password = document.querySelector('#password').value;

			this.postData('/api/sign-in/', { username, password })
				.then(({ data, status }) => {
					location.assign(`/`)
				})
				.catch((error) => {
					console.error("Ошибка входа:", error);
					alert("Неверный логин или пароль.");
				})
		}
	},
	data() {
		return {}
	}
}