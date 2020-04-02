from django.shortcuts import render, HttpResponse
from .forms import PostForm
from .models import Post

# Create your views here.
def index_view(request):
    posts = Post.objects.all()
    losts = []
    founds = []
    active = 0
    for post in posts:
        if post.type == 'lost':
            losts.append(post)
        else:
            founds.append(post)
            if post.is_active:
                active += 1
    context = {
        'losts' : losts,
        'founds' : founds,
        'active' : active,
        'closed' : len(founds) - active
    }
    return render(request, 'index.html', context)

def create_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            if request.user.is_authenticated:
                post.user = request.user
            else:
                post.key = request.POST.get('key')
            post.save()
    else:
        form = PostForm()
    return render(request, 'create.html', {
        'form' : form
    })