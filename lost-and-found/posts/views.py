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


class CreateView(View):
    template_name = 'create.html'
    context = {}
    def get(self, request):
        form = PostForm()
        self.context['form'] = form
        return render(request, self.template_name, self.context)

    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            if request.user.is_authenticated:
                post.user = request.user
            else:
                post.key = request.POST.get('key')
            post.save()

        self.context['form'] = form
        return render(request, self.template_name, self.context)

class DetailView(View):
    template_name = 'detail.html'
    context = {}
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)

        self.context['post'] = post

        return render(request, self.template_name, self.context)

    #def post(self, request, post_id):

class EditPostView(View):
    template_name = 'edit_post.html'

    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)

        return render(request, self.template_name, {
            'post' : post
        })
