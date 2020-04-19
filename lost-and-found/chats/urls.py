from django.urls import path
from .views import ChatIndexView, chat_api, message_api
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(ChatIndexView.as_view()), name='chat_index'),
    path('chat_api/', chat_api, name='chat_api'),
    path('message_api/<int:user_id>/', message_api, name='message_api')
]