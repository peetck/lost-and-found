from django.urls import path
from .views import ChatIndexView, ChatToView

urlpatterns = [
    path('', ChatIndexView.as_view(), name='chat_index'),
    path('<int:user_id>/', ChatToView.as_view(), name='chat_to')
]