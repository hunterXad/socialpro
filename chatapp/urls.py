from django.urls import path 
from .views import *
from django.conf.urls.static import static
from django.conf import settings




urlpatterns = [
    path('rooms/', ChatView.as_view(), name='chat_rooms'),
    path('room/<int:room_id>/', ChatView.as_view(), name='chat_room'),
    path('create/', CreateChatRoomView.as_view(), name='create_chat_room'),
    path('delete/<int:chat_room_id>/', DeleteChatRoomView.as_view(), name='delete_chat_room'),
]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
