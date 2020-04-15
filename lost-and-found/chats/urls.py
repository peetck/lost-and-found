from django.urls import path
from .views import ChatIndexView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(ChatIndexView.as_view()), name='chat_index'),
]