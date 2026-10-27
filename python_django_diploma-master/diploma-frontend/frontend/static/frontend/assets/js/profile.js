var mix = {
	methods: {
		loadProfile() {
			this.getData('/api/profile/')
				.then(data => {
					this.fullName = data.full_name || '';
					this.phone = data.phone || '';
					this.email = data.email || '';
					if (data.avatar) {
						this.avatar = { src: data.avatar, alt: 'Аватар' };
					}
				})
				.catch(err => console.error("Ошибка загрузки профиля:", err));
		},
		changeProfile() {
			const formData = new FormData();
			// В Django REST Framework поля ожидаются под теми же именами, что и в модели
			formData.append('full_name', this.fullName);
			formData.append('phone', this.phone);
			formData.append('email', this.email);

			const fileInput = document.querySelector('#avatar');
			if (fileInput && fileInput.files.length > 0) {
				formData.append('avatar', fileInput.files[0]);
			}

			// Используем чистый axios, чтобы он сам выставил правильный boundary для multipart
			axios.post('/api/profile/', formData, {
				headers: {
					'X-CSRFToken': this.getCookie('csrftoken'),
					// Content-Type указывать НЕ НАДО, Axios сделает это сам!
				}
			})
			.then(({ data }) => {
				alert(data.message);
				this.loadProfile();
			})
			.catch(error => {
				console.error("Ошибка обновления профиля:", error.response.data);
				alert("Ошибка: " + JSON.stringify(error.response.data));
			});
		},
		changePassword() {
			const payload = {
				passwordCurrent: this.passwordCurrent,
				password: this.password,
				passwordReply: this.passwordReply
			};

			this.postData('/api/profile/change-password/', payload)
				.then(({ data }) => {
					alert(data.message);
					this.passwordCurrent = '';
					this.password = '';
					this.passwordReply = '';
				})
				.catch(error => {
					console.error("Ошибка смены пароля:", error);
					alert("Ошибка: " + JSON.stringify(error.response.data));
				});
		},
		setAvatar(event) {
			const file = event.target.files[0];
			if (file) {
				if (file.size > 2 * 1024 * 1024) {
					alert("Размер аватарки не должен превышать 2 Мб");
					return;
				}
				this.avatar = { src: URL.createObjectURL(file), alt: 'Аватар' };
			}
		},
		clearAvatar() {
			this.avatar = null;
		}
	},
	mounted() {
		this.loadProfile();
	},
	data() {
		return {
			fullName: '',
			phone: '',
			email: '',
			avatar: null,
			passwordCurrent: '',
			password: '',
			passwordReply: ''
		}
	}
}