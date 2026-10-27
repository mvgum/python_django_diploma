from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    name = serializers.CharField(required=False)  # Принимаем 'name' от фронтенда

    class Meta:
        model = User
        fields = ('username', 'name', 'password')

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data.get('email', f"{username}@example.com")
        name = validated_data.get('name', '')

        user = User.objects.create_user(
            username=username,
            email=email,
            full_name=name,
            password=validated_data['password']
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'full_name', 'phone', 'avatar')

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('full_name', 'phone', 'email', 'avatar')

    def validate_avatar(self, value):
        if value and value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError("Размер аватарки не должен превышать 2 Мб")
        return value

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует")
        return value

    def validate_phone(self, value):
        user = self.context['request'].user
        if value and User.objects.exclude(pk=user.pk).filter(phone=value).exists():
            raise serializers.ValidationError("Пользователь с таким телефоном уже существует")
        return value

class PasswordChangeSerializer(serializers.Serializer):
    passwordCurrent = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    passwordReply = serializers.CharField(required=True)

    def validate(self, data):
        if data['password'] != data['passwordReply']:
            raise serializers.ValidationError({"passwordReply": "Пароли не совпадают"})
        return data
