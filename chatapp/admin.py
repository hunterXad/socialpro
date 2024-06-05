from django.contrib import admin
from .models import ChatRoom

class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at')  # Example fields

admin.site.register(ChatRoom, ChatRoomAdmin)
