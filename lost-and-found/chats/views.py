from django.shortcuts import render
from django.contrib.auth.models import User
from django.views import View
from .models import Message

from django.http import JsonResponse
import json

# Create your views here.

def chat_api(request):
    if request.method == 'POST':
        users = User.objects.all()
        data = []
        for user in users:
            if user == request.user:
                continue
            sends = user.chat.message_set.all()
            gets = Message.objects.filter(to=user)

            if len(sends) != 0 and len(gets) != 0:
                last_send_msg = sends.order_by('-timestamp')[0]
                last_get_msg = gets.order_by('-timestamp')[0]
                if last_send_msg.timestamp > last_get_msg.timestamp:
                    message = last_send_msg.message
                    datetime = last_send_msg.timestamp
                else:
                    message = last_get_msg.message
                    datetime = last_get_msg.timestamp
            elif len(sends) != 0:
                last_send_msg = sends.order_by('-timestamp')[0]
                message = last_send_msg.message
                datetime = last_send_msg.timestamp
            elif len(gets) != 0:
                last_get_msg = gets.order_by('-timestamp')[0]
                message = last_get_msg.message
                datetime = last_get_msg.timestamp
            else:
                message = ''
                datetime = ''
            data.append([user.username, message, datetime, user.userprofile.avatar.url, user.id])

        return JsonResponse({'users' : data})

class ChatIndexView(View):
    template_name = 'chat_index.html'

    def get(self, request):
        return render(request, self.template_name, {})

