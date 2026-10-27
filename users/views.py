from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .serializers import UserRegisterSerializer, UserProfileSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import UserUpdateSerializer, PasswordChangeSerializer


@method_decorator(csrf_exempt, name='dispatch')
class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response({'message': 'Успешная регистрация'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class SignInView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')  # Теперь ждем 'username'
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'message': 'Успешный вход'}, status=status.HTTP_200_OK)
        return Response({'error': 'Неверный логин или пароль'}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class SignOutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Вы вышли из системы'}, status=status.HTTP_200_OK)


class ProfileView(APIView):
    parser_classes = (MultiPartParser, FormParser)  # Чтобы принимать файлы (аватарки)

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Неавторизован'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Неавторизован'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Профиль успешно обновлен', 'user': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Неавторизован'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['passwordCurrent']):
                return Response({'passwordCurrent': ['Неверный текущий пароль']}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({'message': 'Пароль успешно изменен'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
