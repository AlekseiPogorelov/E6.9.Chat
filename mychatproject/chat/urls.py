from django.urls import path
from . import views

urlpatterns = [
    path('<int:room_name>/', views.chat_room, name='chat_room'),
]