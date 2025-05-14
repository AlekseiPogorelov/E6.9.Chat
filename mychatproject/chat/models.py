from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, default='avatars/default_avatar.png')
    display_name = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()


class ChatRoom(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='chat_avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_chatrooms')
    participants = models.ManyToManyField(User, related_name='chatrooms')
    is_group = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    chat = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'From {self.sender.username} in {self.chat.name} at {self.timestamp}'

