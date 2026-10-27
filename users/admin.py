from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'full_name', 'phone', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительно', {'fields': ('full_name', 'phone', 'avatar')}),
    )
