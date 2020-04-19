from django.shortcuts import render
from django.contrib.auth.models import User
from django.views import View
from .models import Message
from .serializers import MessageSerializer
from django.http import JsonResponse
import json

# Create your views here.

def chat_api(request):
    if request.method == 'GET':
        users = User.objects.all()
        data = []
        for user in users:
            if user == request.user:
                continue
            sends = request.user.chat.message_set.filter(to=user).order_by('-timestamp')
            gets = Message.objects.filter(chat=user.chat, to=request.user).order_by('-timestamp')

            print(sends, gets)

            message = ''
            datetime = ''

            if len(sends) != 0 and len(gets) != 0:
                if sends[0].timestamp > gets[0].timestamp:
                    message = sends[0].message
                    datetime = sends[0].timestamp
                else:
                    message = gets[0].message
                    datetime = gets[0].timestamp
            elif len(sends) != 0:
                message = sends[0].message
                datetime = sends[0].timestamp
            elif len(gets) != 0:
                message = gets[0].message
                datetime = gets[0].timestamp

            data.append([user.username, message, datetime, user.userprofile.avatar.url, user.id])
        return JsonResponse(data, safe=False)

def message_api(request, user_id):
    if request.method == 'GET':
        user = User.objects.get(id=user_id)

        # get conversation msg

        sends = request.user.chat.message_set.filter(to=user).order_by('timestamp')
        gets = Message.objects.filter(chat=user.chat, to=request.user).order_by('timestamp')

        sends_serializer = MessageSerializer(sends, many=True)
        gets_serializer = MessageSerializer(gets, many=True)
        # return
        return JsonResponse({
            'sends' : sends_serializer.data,
            'gets' : gets_serializer.data
            })
    if request.method == 'POST':
        user = User.objects.get(id=user_id)

        data = json.loads(request.body)

        message = Message.objects.create(
            message=data.get('message'),
            seen=False,
            chat=request.user.chat,
            to=user
        )

        return JsonResponse(MessageSerializer(message).data)

class ChatIndexView(View):
    template_name = 'chat_index.html'

    def get(self, request):
        return render(request, self.template_name, {})

