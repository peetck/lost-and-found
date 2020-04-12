from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from django.views import View
from .models import Message

# Create your views here.

class ChatIndexView(View):
    template_name = 'chat_index.html'

    def get(self, request):
        users = User.objects.all().exclude(id=request.user.id)

        context = {
            'users' : users
        }
        return render(request, self.template_name, context)

class ChatToView(View):
    template_name = 'chat_to.html'

    def get(self, request, user_id):
        user = User.objects.get(id=user_id)

        send_messages = request.user.chat.message_set.all()
        get_messages = user.chat.message_set.all()
        return render(request, self.template_name, {
            'user' : user,
            'send_messages' : send_messages,
            'get_messages' : get_messages
        })

    def post(self, request, user_id):

        user = User.objects.get(id=user_id)

        Message.objects.create(
            message=request.POST.get('msg'),
            seen=False,
            to=user,
            chat=request.user.chat
        )

        send_messages = request.user.chat.message_set.all()
        get_messages = user.chat.message_set.all()

        return render(request, self.template_name, {
            'user' : user,
            'send_messages' : send_messages,
            'get_messages' : get_messages
        })