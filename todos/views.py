# import libraries
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from .serializers import UserSerializer, LoginSerializer
from .models import Todo
from .serializers import TodoSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication

class TodoViewSet(viewsets.ViewSet):
    """TodoViewSet"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TodoSerializer

    # create todo
    def create(self, request):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            todo = serializer.save()
            return Response({'data': {'todo': serializer.data}, 'message': 'success', 'status_code': 201}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Get list of todos
    def list(self, request):

        todos = Todo.objects.all()
        serializer = self.serializer_class(todos, many=True)
        return Response({'data': serializer.data, 'status_code': 200}, status=status.HTTP_200_OK)

    # Retrieve todo
    def retrieve(self, request, pk=None):

        try:
            todo = Todo.objects.get(pk=pk)
            serializer = self.serializer_class(todo)
            return Response({'data': serializer.data, 'status_code': 200}, status=status.HTTP_200_OK)
        except Todo.DoesNotExist:
            return Response({'error': 'Todo invalid.', 'status_code': 404}, status=status.HTTP_404_NOT_FOUND)
        
    # Upadate todo
    def update(self, request, pk=None):

        try:
            todo = Todo.objects.get(pk=pk)
            serializer = self.serializer_class(todo, data=request.data, partial=True)
            if serializer.is_valid():
                todo = serializer.save()
                return Response({'data': {'todo': serializer.data}, 'message': 'updated success', 'status_code': 200}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Todo.DoesNotExist:
            return Response({'error': 'Todo invalid.', 'status_code': 404}, status=status.HTTP_404_NOT_FOUND)

    # Destroy todo
    def destroy(self, request, pk=None):

        try:
            todo = Todo.objects.get(pk=pk)
            todo.delete()
            return Response({'message': 'Todo deteled success', 'status_code': 204}, status=status.HTTP_204_NO_CONTENT)
        except Todo.DoesNotExist:
            return Response({'error': 'Todo invalid', 'status_code': 404}, status=status.HTTP_404_NOT_FOUND)


class UserViewSet(viewsets.ViewSet):

    # Create user
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user_data = UserSerializer(user).data
            return Response({'data': {'user': user_data}, 'message': 'Created user successfully', 'status_code': 201}, status=status.HTTP_201_CREATED)

        # check error
        if 'username' in serializer.errors:
            return Response({'error': 'User exit.', 'status_code': 400}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Get list of user
    def list(self, request):
        if request.user.is_authenticated:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response({'data': serializer.data, 'status_code': 200}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User not authenticated.', 'status_code': 401}, status=status.HTTP_401_UNAUTHORIZED)

    # retrieve user
    def retrieve(self, request, pk=None):
        if request.user.is_authenticated:
            try:
                user = User.objects.get(pk=pk)
                serializer = UserSerializer(user)
                return Response({'data': serializer.data, 'status_code': 200}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'error': 'User does not exist', 'status_code': 404}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'User not authenticated', 'status_code': 401}, status=status.HTTP_401_UNAUTHORIZED)

    # Update user
    def update(self, request, pk=None):
        if request.user.is_authenticated:
            try:
                user = User.objects.get(pk=pk)
                serializer = UserSerializer(
                    user, data=request.data, partial=True)
                if serializer.is_valid():
                    user = serializer.save()
                    user_data = UserSerializer(user).data
                    return Response({'data': {'user': user_data}, 'message': 'User updated successfully', 'status_code': 200}, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({'error': 'User does not exist.', 'status_code': 404}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'User not authenticated', 'status_code': 401}, status=status.HTTP_401_UNAUTHORIZED)

    # Destroy User
    def destroy(self, request, pk=None):
        if request.user.is_authenticated:
            try:
                user = User.objects.get(pk=pk)
                user.delete()
                return Response({'message': 'User deleted successfull ', 'status_code': 204}, status=status.HTTP_204_NO_CONTENT)
            except User.DoesNotExist:
                return Response({'error': 'User does not exist.', 'status_code': 404}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'User not authenticated', 'status_code': 401}, status=status.HTTP_401_UNAUTHORIZED)

