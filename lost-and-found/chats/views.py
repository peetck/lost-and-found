from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from django.views import View
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
        return render(request, self.template_name, {
            'user_id' : user_id
        })