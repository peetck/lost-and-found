from django.shortcuts import render, HttpResponse

# Create your views here.
def chat_index_view(request):
    return HttpResponse('Chat Index Page!')

def chat_to_view(request, user_id):
    return HttpResponse(f'Chat To {user_id}')