from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ProfileViewSet, ChatRoomViewSet, MessageViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'profile', ProfileViewSet, basename='profile')
router.register(r'chats', ChatRoomViewSet, basename='chatroom')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]