from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

# Импорты вьюх
from catalog import views as catalog_views
from users import views as user_views
from cart import views as cart_views
from orders import views as order_views

# --- API ПУТИ (все, что начинается с /api/) ---
api_patterns = [
    # Каталог
    path('categories/', catalog_views.CategoryListView.as_view()),
    path('catalog/', catalog_views.CatalogListView.as_view()),
    path('catalog/filters/<int:category_id>/', catalog_views.CatalogFiltersView.as_view()),
    path('product/<int:pk>/', catalog_views.ProductDetailView.as_view()),
    path('products/popular/', catalog_views.PopularProductsView.as_view()),
    path('products/limited/', catalog_views.LimitedProductsView.as_view()),
    path('banners/', catalog_views.BannerListView.as_view()),
    path('tags/', catalog_views.TagListView.as_view()),  # Заглушка для тегов

    # Пользователи
    path('sign-up/', user_views.SignUpView.as_view()),
    path('sign-in/', user_views.SignInView.as_view()),
    path('sign-out/', user_views.SignOutView.as_view()),
    path('profile/', user_views.ProfileView.as_view()),
    path('profile/change-password/', user_views.PasswordChangeView.as_view()),

    # Корзина
    path('basket/', cart_views.BasketView.as_view()),

    # Заказы
    path('orders/', order_views.OrderCreateView.as_view()),  # Создание (POST)
    path('orders/preview/', order_views.OrderPreviewView.as_view()),  # Предпросмотр (GET)
    path('orders/list/', order_views.OrderListView.as_view()),  # История (GET)

    # Детали и оплата
    path('order/<int:pk>/', order_views.OrderDetailView.as_view()),  # Детали (GET)
    path('payment/<int:pk>/', order_views.PaymentView.as_view()),  # Оплата (POST)
]

# --- HTML СТРАНИЦЫ ---
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_patterns)),  # Подключаем все API-пути

    # Страницы заказов
    path('orders/<int:pk>/', TemplateView.as_view(template_name="frontend/oneorder.html")),  # Детали
    path('orders/', TemplateView.as_view(template_name="frontend/order.html")),  # Оформление
    path('history-order/', TemplateView.as_view(template_name="frontend/historyorder.html")),  # История

    # Подключаем остальные страницы фронтенда (главная, каталог и т.д.)
    path("", include("frontend.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
