from django.contrib.auth import login
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Profile, ChatRoom, Message
from .forms import SignUpForm
from .serializers import (
    UserSerializer, ProfileSerializer, ProfileUpdateSerializer,
    ChatRoomSerializer, ChatRoomCreateUpdateSerializer,
    MessageSerializer
)

def home(request):
    user_chats = request.user.chatrooms.all() \
        if request.user.is_authenticated \
        else []
    return render(request, 'core/home.html', {'chatrooms': user_chats})


def profile_redirect(request):
    return redirect('home')

# Вьюсет для пользователей (только просмотр списка и деталей)
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

# Вьюсет для профиля текущего пользователя
class ProfileViewSet(viewsets.GenericViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return ProfileUpdateSerializer
        return ProfileSerializer

    def retrieve(self, request):
        profile = request.user.profile
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    def update(self, request):
        profile = request.user.profile
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    partial_update = update

# Вьюсет для управления чатами
class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ChatRoomCreateUpdateSerializer
        return ChatRoomSerializer

    def perform_create(self, serializer):
        chatroom = serializer.save(owner=self.request.user)
        # Добавляем создателя в участников
        chatroom.participants.add(self.request.user)

    def get_queryset(self):
        # Пользователь видит только чаты, в которых он участвует
        return self.request.user.chatrooms.all()

# Вьюсет для сообщений
class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Получаем сообщения только из чатов, в которых пользователь участвует
        chat_id = self.request.query_params.get('chat')
        if chat_id:
            chat = ChatRoom.objects.filter(id=chat_id, participants=self.request.user).first()
            if chat:
                return chat.messages.all()
            else:
                return Message.objects.none()
        return Message.objects.none()

    def perform_create(self, serializer):
        chat_id = self.request.data.get('chat')
        chat = ChatRoom.objects.filter(id=chat_id, participants=self.request.user).first()
        if not chat:
            raise PermissionError("Вы не участник этого чата")
        serializer.save(sender=self.request.user, chat=chat)

def chat_room(request, room_name):
    room = get_object_or_404(ChatRoom, id=room_name)
    return render(request, 'chat/chat_room.html', {'room': room})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Можно сразу логинить пользователя
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form': form})