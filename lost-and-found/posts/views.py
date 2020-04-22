from django.shortcuts import render, redirect
from .forms import PostForm, PostPictureForm
from django.http import JsonResponse
from .models import Post, PostPicture
from django.views import View
from django.forms import formset_factory

from .serializers import PostSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class PostAPI(APIView):

    def get(self, request):
        posts = Post.objects.filter(is_active=True)

        serializer_posts = PostSerializer(posts, many=True)

        return Response(serializer_posts.data, status=status.HTTP_200_OK)

class IndexView(View):
    template_name = 'index.html'
    def get(self, request):
        posts = Post.objects.filter(is_active=True)
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

        return render(request, self.template_name, {
            'losts' : losts,
            'founds' : founds,
            'active' : active,
            'closed' : len(founds) - active,
            'all' : len(founds) + len(losts)
        })


class CreateView(View):
    template_name = 'create.html'
    PictureFormSet = formset_factory(PostPictureForm, extra=0)
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
                            'key_error' : 'มีคีย์นี้อยู่ในระบบแล้ว'
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
        form = PostForm(instance=post)

        if request.user != post.user:
            return redirect('index')


        return render(request, self.template_name, {
            'form' : form,
            'post': post,
            'anonymous' : True if post.user == None else False
        })

    def post(self, request, post_id):

        post = Post.objects.get(id=post_id)
        form = PostForm(request.POST, instance=post)

        if form.is_valid():

            post = form.save(commit=False)
            is_active = request.POST.get('is_active')
            if is_active:
                post.is_active = True
            else:
                post.is_active = False

            if post.user == None and request.POST.get('key') != post.key:
                return render(request, self.template_name, {
                    'form' : form,
                    'post': post,
                    'anonymous' : True if post.user == None else False,
                    'key_error' : 'คีย์ที่กรอกมาไม่ถูกต้อง'
                })

            post.save()

            return render(request, self.template_name, {
                'form' : form,
                'post': post,
                'anonymous' : True if post.user == None else False
             })



def delete_view(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('my_posts')
