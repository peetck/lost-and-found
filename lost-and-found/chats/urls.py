from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_index_view, name='chat_index'),
    path('<int:user_id>/', views.chat_to_view, name='chat_to')
]