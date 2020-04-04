from django.shortcuts import render, HttpResponse
from .forms import PostForm
from .models import Post
from django.views import View
# Create your views here.

class IndexView(View):
    context = {}
    template_name = 'index.html'
    def get(self, request):
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

        self.context['losts'] = losts
        self.context['founds'] = founds
        self.context['active'] = active
        self.context['closed'] = len(founds) - active

        return render(request, self.template_name, self.context)


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