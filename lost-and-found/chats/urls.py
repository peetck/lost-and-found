from django.urls import path
from .views import ChatIndexView, ChatAPI, MessageAPI

urlpatterns = [
    path('', ChatIndexView.as_view(), name='chat_index'),
    path('chat_api/', ChatAPI.as_view(), name='chat_api'),
    path('message_api/<int:user_id>/', MessageAPI.as_view(), name='message_api')
]