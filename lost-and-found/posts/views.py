from django.shortcuts import render, redirect
from .forms import PostForm, PostPictureForm
from django.http import JsonResponse
from .models import Post, PostPicture, AssetType
from django.views import View
from django.forms import formset_factory

from .serializers import PostSerializer, AssetTypeSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from datetime import datetime
# Create your views here.

class PostAPI(APIView):

    def get(self, request):
        search_title = request.GET.get('search_title')
        search_location = request.GET.get('search_location')
        search_assetType = int(request.GET.get('search_assetType'))
        search_date = request.GET.get('search_date')

        if search_date != '' and search_assetType != -1:
            date_time = datetime.strptime(search_date, "%d/%m/%Y")
            posts = Post.objects.filter(
                is_active=True,
                title__icontains=search_title,
                location__icontains=search_location,
                assetType=AssetType.objects.get(id=search_assetType),
                date_time__year=date_time.year,
                date_time__month=date_time.month,
                date_time__day=date_time.day
            ).order_by('-create_at') # sort by create_at desc
        elif search_date != '':
            date_time = datetime.strptime(search_date, "%d/%m/%Y")
            posts = Post.objects.filter(
                is_active=True,
                title__icontains=search_title,
                location__icontains=search_location,
                date_time__year=date_time.year,
                date_time__month=date_time.month,
                date_time__day=date_time.day
            ).order_by('-create_at') # sort by create_at desc
        elif search_assetType != -1:
            posts = Post.objects.filter(
                is_active=True,
                title__icontains=search_title,
                location__icontains=search_location,
                assetType=AssetType.objects.get(id=search_assetType)
            ).order_by('-create_at') # sort by create_at desc
        else:
            posts = Post.objects.filter(
                is_active=True,
                title__icontains=search_title,
                location__icontains=search_location,
            ).order_by('-create_at') # sort by create_at desc

        assetTypes = AssetType.objects.all()

        serializer_posts = PostSerializer(posts, many=True)
        serializer_assetTypes = AssetTypeSerializer(assetTypes, many=True)

        return Response([serializer_posts.data, serializer_assetTypes.data], status=status.HTTP_200_OK)

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
            if request.POST.get('form-TOTAL_FORMS') != '0':
                for picture in formset:
                    if picture.is_valid():
                        picture = picture.save(commit=False)
                        picture.post = post
                        picture.save()
            return redirect('detail', post_id=post.id)
        else:
            return render(request, self.template_name, {
                'form' : form
            })

class DetailView(View):
    template_name = 'detail.html'
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)

        return render(request, self.template_name, {
            'post' : post
        })

    #def post(self, request, post_id):

class EditPostView(View):
    template_name = 'edit_post.html'
    PictureFormSet = formset_factory(PostPictureForm, extra=0)

    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)

        form = PostForm(instance=post)

        if request.user != post.user:
            return redirect('index')


        formset = self.PictureFormSet()


        return render(request, self.template_name, {
            'form' : form,
            'post': post,
            'pictures' : post.postpicture_set.all(),
            'formset' : formset,
            'anonymous' : True if post.user == None else False,
        })

    def post(self, request, post_id):

        post = Post.objects.get(id=post_id)
        form = PostForm(request.POST, instance=post)

        formset = self.PictureFormSet(request.POST, request.FILES)

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

            # ถ้า มีการกดลบรูป (JS จะ set value ของ input:hidden เป็น 0)
            for picture in post.postpicture_set.all():
                value = request.POST.get(f'{picture.id}')
                if value == '0':
                    picture.delete()

            if request.POST.get('form-TOTAL_FORMS') != '0':
                for picture in formset:
                    if picture.is_valid():
                        picture = picture.save(commit=False)
                        picture.post = post
                        picture.save()

            return redirect('edit_post', post_id)



def delete_view(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('my_posts')
