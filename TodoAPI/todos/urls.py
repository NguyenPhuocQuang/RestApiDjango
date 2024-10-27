from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserViewSet,TodoViewSet

user_list = UserViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

user_detail = UserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

todo_list = TodoViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

todo_detail = TodoViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

urlpatterns = [
    path('users', user_list, name='user-list'),
    path('users/<int:pk>', user_detail, name='user-detail'),
    
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),    
    
    path('todos', todo_list, name='todo-list'),
    path('todos/<int:pk>', todo_detail, name='todo-detail'),
]


