from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, ChatRoom, Message

# Сериализатор для профиля пользователя
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['display_name', 'avatar']

# Сериализатор для пользователя с вложенным профилем
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']

# Сериализатор для создания/обновления профиля
class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['display_name', 'avatar']

# Сериализатор для сообщений
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'chat', 'sender', 'content', 'timestamp']
        read_only_fields = ['id', 'sender', 'timestamp']

# Сериализатор для группового чата
class ChatRoomSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    participants = UserSerializer(many=True, read_only=True)

    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'description', 'avatar', 'owner', 'participants', 'created_at', 'updated_at']

# Сериализатор для создания/обновления чата с возможностью указать участников по id
class ChatRoomCreateUpdateSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = ChatRoom
        fields = ['name', 'description', 'avatar', 'participants']
