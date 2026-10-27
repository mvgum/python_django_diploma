from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import FileExtensionValidator

def validate_avatar_size(image):
    if image.size > 2 * 1024 * 1024:
        raise ValueError("Размер аватарки не должен превышать 2 Мб")

class User(AbstractUser):
    full_name = models.CharField(max_length=255, verbose_name="ФИО", blank=True)
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name="Телефон")
    email = models.EmailField(unique=True, verbose_name="Email")
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png']), validate_avatar_size],
        verbose_name="Аватар"
    )

    REQUIRED_FIELDS = ['email']

