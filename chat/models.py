from django.db import models


class ChatMessage(models.Model):
    user_input = models.TextField(blank=True, null=True)
    bot_response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user_ip = models.GenericIPAddressField(null=True, blank=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Pergunta em {self.created_at.strftime('%d/%m/%Y %H:%M:%S')}"
