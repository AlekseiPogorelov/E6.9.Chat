"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from chat.views import home, chat_room
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls')),       # Веб-маршруты
    path('api/', include('chat.api_urls')),    # API-маршруты
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('chat/private/<int:user_id>/', views.private_chat, name='private_chat'),
    path('chat/<int:room_id>/', chat_room, name='chat_room'),
    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
