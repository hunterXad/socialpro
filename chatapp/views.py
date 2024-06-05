from django.shortcuts import render, redirect , get_object_or_404, redirect
from django.views import View
from .forms import ChatRoomForm 
import json
from django.http import JsonResponse
from .models import ChatRoom, Message
from django.utils import timezone
from django.http import HttpResponseNotAllowed
from django.urls import reverse

class ChatView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, room_id=None):
        rooms = ChatRoom.objects.all().order_by('-created_at')
        room = None
        messages = []
        if room_id:
            room = get_object_or_404(ChatRoom, id=room_id)
            messages = Message.objects.filter(room=room).order_by('timestamp')
        return render(request, 'chat_room.html', {'rooms': rooms, 'room': room, 'messages': messages})

    def post(self, request, room_id):
        room = get_object_or_404(ChatRoom, id=room_id)
        content = request.POST.get('content')
        if content:
            message = Message.objects.create(room=room, sender=request.user, content=content, timestamp=timezone.now())
            message_data = {
                'sender': message.sender.username,
                'content': message.content,
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'profile_image': message.sender.profile.image.url if message.sender.profile.image else None
            }
            # استخدام reverse للحصول على عنوان URL بناءً على اسم المسار
            return redirect('chat_room', room_id=room.id)

        return JsonResponse({'error': 'Invalid request'}, status=400)

class CreateChatRoomView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  
        return super().dispatch(request, *args, **kwargs)
    def get(self, request):
        form = ChatRoomForm()
        return render(request, 'create_chat_room.html', {'form': form})

    
    def post(self, request):
        form = ChatRoomForm(request.POST, request.FILES)
        if form.is_valid():
            chat_room = form.save(commit=False)
            chat_room.created_by = request.user
            chat_room.created_at = timezone.now()
            chat_room.save()
            return redirect('chat_rooms')
        return render(request, 'create_chat_room.html', {'form': form})

class DeleteChatRoomView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, chat_room_id):
        chat_room = get_object_or_404(ChatRoom, id=chat_room_id)
        if chat_room.created_by == request.user:  
            chat_room.delete()
        return redirect('chat_rooms')
