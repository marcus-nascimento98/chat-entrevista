from django.shortcuts import render
from chat.models import ChatMessage
from django.shortcuts import redirect
from ai.agent import AIBot
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

ai_bot = AIBot()

def index(request):
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key

    history = ChatMessage.objects.filter(session_id=session_id).order_by('created_at')
    return render(request, 'chat/index.html', {'history': history})

@require_POST
def chat_api(request):
    user_message = request.POST.get('user_message')
    session_id = request.session.session_key
    
    if not session_id:
        request.session.create()
        session_id = request.session.session_key
    
    ChatMessage.objects.create(
        user_input=user_message,
        session_id=session_id,
    )
    
    history_message = ChatMessage.objects.filter(session_id=session_id).order_by('-created_at')[:10]
    
    ai_message = ai_bot.invoke(user_message, history_message)
    
    ChatMessage.objects.create(
        bot_response=ai_message,
        session_id=session_id,
    )
    
    return JsonResponse({
        'bot_response': ai_message
    })