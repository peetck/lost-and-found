from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User

# Create your views here.
def chat_index_view(request):
    users = User.objects.all().exclude(id=request.user.id)

    context = {
        'users' : users
    }
    return render(request, 'chat_index.html', context)

def chat_to_view(request, user_id):
    return render(request, 'chat_to.html', {
        'user_id' : user_id
    })