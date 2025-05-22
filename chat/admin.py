from django.contrib import admin
from chat.models import ChatMessage


class ChatAdmin(admin.ModelAdmin):
    list_display = ('user_input', 'bot_response', 'created_at', 'user_ip', 'session_id',)

admin.site.register(ChatMessage, ChatAdmin)
