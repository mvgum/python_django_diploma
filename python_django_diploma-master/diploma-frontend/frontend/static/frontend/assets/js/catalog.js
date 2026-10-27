var mix = {
    methods: {
        setTag (id) {
            this.topTags = this.topTags.map(tag => {
                return  tag.id === id
                    ? {
                        ...tag,
                        selected: !tag.selected
                    }
                    : tag
            })
            this.getCatalogs()
        },
        setSort (id) {
            if (this.selectedSort?.id === id) {
                this.selectedSort.selected =
                    this.selectedSort.selected === 'dec'
                        ? 'inc'
                        : 'dec'
            } else {
                if (this.selectedSort) {
                    this.selectedSort = null
                }
                this.selectedSort = this.sortRules.find(sort => sort.id === id)
                this.selectedSort = {
                    ...this.selectedSort,
                    selected: 'dec'
                }
            }
            this.getCatalogs()
        },
        getTags() {
            this.getData('/api/tags/', { category: this.category })
                .then(data => this.topTags = data.map(tag => ({
                    ...tag,
                    selected: false
                })))
                .catch(() => {
                        this.topTags = []
                        console.warn('Ошибка получения тегов')
                })
        },
		getCatalogs(page = 1) {
			// Собираем все параметры из фильтров и сортировки
			const params = {
				page: page,
				title: this.filter.name || '',
//				minPrice: this.filter.minPrice || '',
//				maxPrice: this.filter.maxPrice || '',
				sort: this.selectedSort ? this.selectedSort.id : 'popular',
				sortType: this.selectedSort ? this.selectedSort.selected : 'dec'
			};

			// Преобразуем {name: '...'} в {'filter[name]': '...'}
			const queryParams = {};
			for (const key in params) {
				if (['name', 'minPrice', 'maxPrice'].includes(key)) {
					queryParams[`filter[${key}]`] = params[key];
				} else {
					queryParams[key] = params[key];
				}
			}

			this.getData('/api/catalog/', queryParams)
				.then(data => {
					// ИСПРАВЛЕНО: Берем массив из поля results
					this.catalogCards = data.results || [];
					this.currentPage = page;
					// Считаем общее количество страниц (20 товаров на страницу)
					this.lastPage = Math.ceil((data.count || 0) / 20);

					if (this.catalogCards.length === 0) {
						console.warn("Товары не найдены по заданным фильтрам");
					}
				})
				.catch(err => console.error("Ошибка каталога:", err));
		}
    },
    mounted() {
        this.selectedSort = this.sortRules?.[1]
            ? { ...this.sortRules?.[1], selected: 'inc' }
            :  null

        if(location.pathname.startsWith('/catalog/')) {
            const category = location.pathname.replace('/catalog/', '')
            this.category = category.length ? Number(category) : null
        }

        this.getCatalogs()
        this.getTags()
    },
    data() {
        return {
            category: null,
            catalogCards: [],
            currentPage: null,
            lastPage: 1,
            selectedSort: null,
            filter: {
                name: '',
                minPrice: 0,
                maxPrice: 50000,
                freeDelivery: false,
                available: true
            }
        }
    }
}