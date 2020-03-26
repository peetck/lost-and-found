from django.shortcuts import render, HttpResponse

# Create your views here.
def chat_index_view(request):
    return render(request, 'chat_index.html')

def chat_to_view(request, user_id):
    return render(request, 'chat_to.html', {
        'user_id' : user_id
    })