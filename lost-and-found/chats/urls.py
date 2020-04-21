from django.urls import path
from .views import ChatIndexView, ChatAPI, MessageAPI
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(ChatIndexView.as_view()), name='chat_index'),
    path('chat_api/', ChatAPI.as_view(), name='chat_api'),
    path('message_api/<int:user_id>/', MessageAPI.as_view(), name='message_api')
]