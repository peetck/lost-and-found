from django.shortcuts import render, HttpResponse
from .forms import PostForm

# Create your views here.
def index_view(request):
    return render(request, 'index.html')

def create_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
    else:
        form = PostForm()
    return render(request, 'create.html', {
        'form' : form
    })