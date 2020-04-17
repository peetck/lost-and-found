from django.shortcuts import render, redirect
from .forms import PostForm, PostPictureForm
from .models import Post, PostPicture
from django.views import View
from django.forms import formset_factory

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
        self.context['all'] = len(founds) + len(losts)
        return render(request, self.template_name, self.context)


class CreateView(View):
    template_name = 'create.html'
    PictureFormSet = formset_factory(PostPictureForm, extra=1)
    def get(self, request):
        form = PostForm()
        formset = self.PictureFormSet()
        return render(request, self.template_name, {
            'form' : form,
            'formset' : formset
        })

    def post(self, request):
        form = PostForm(request.POST)
        formset = self.PictureFormSet(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            if request.user.is_authenticated:
                post.user = request.user
            else:
                post.key = request.POST.get('key')
                for i in Post.objects.all():
                    if i.key == post.key:
                        return render(request, self.template_name, {
                            'form' : form,
                            'key_error' : 'มี key นี้อยู่ในระบบแล้ว'
                        })
            post.save()
            passed = False
            for picture in formset:
                if picture.is_valid():
                    picture = picture.save(commit=False)
                    if picture.picture == 'posts/default.png' and passed:
                        continue
                    picture.post = post
                    picture.save()
                    passed = True
            return redirect('detail', post_id=post.id)

        return render(request, self.template_name, {
            'form' : form
        })

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

def delete_view(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('my_posts')
