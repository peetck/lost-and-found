from django.urls import path
from .views import ChatIndexView, ChatToView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(ChatIndexView.as_view()), name='chat_index'),
    path('<int:user_id>/', login_required(ChatToView.as_view()), name='chat_to')
]