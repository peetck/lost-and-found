from django.shortcuts import render, redirect
from .forms import PostForm, PostPictureForm
from django.http import JsonResponse
from .models import Post, PostPicture, AssetType, Comment
from django.views import View
from django.forms import formset_factory

from .serializers import PostSerializer, AssetTypeSerializer, CommentSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from datetime import datetime
# Create your views here.

class CommentAPI(APIView):

    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        comments = Comment.objects.filter(post=post)
        serializer_comment = CommentSerializer(comments, many=True)
        return Response(serializer_comment.data, status=status.HTTP_200_OK)



class PostAPI(APIView):

    def get(self, request):
        search_title = request.GET.get('search_title')
        search_location = request.GET.get('search_location')
        posts = Post.objects.filter(title__icontains=search_title, location__icontains=search_location)

        search_date = request.GET.get('search_date')
        if search_date != '':
            date_time = datetime.strptime(search_date, "%d/%m/%Y")
            posts = posts.filter(date_time__year=date_time.year, date_time__month=date_time.month, date_time__day=date_time.day)

        search_assetType = request.GET.get('search_assetType')
        if search_assetType != '-1':
            posts = posts.filter(assetType=AssetType.objects.get(id=search_assetType))

        search_type = request.GET.get('search_type')
        if search_type != '-1':
            posts = posts.filter(type=search_type)

        search_is_active = request.GET.get('search_is_active')
        if search_is_active != '-1':
            posts = posts.filter(is_active=bool(int(search_is_active)))

        posts = posts.order_by('-is_active', '-create_at') # sort by create_at & is_active desc

        assetTypes = AssetType.objects.all()

        serializer_posts = PostSerializer(posts, many=True)
        serializer_assetTypes = AssetTypeSerializer(assetTypes, many=True)

        return Response([serializer_posts.data, serializer_assetTypes.data], status=status.HTTP_200_OK)

    def patch(self, request):
        post_id = request.data.get('post_id')
        post = Post.objects.get(id=post_id)

        post.is_active = False
        post.take_information = request.data.get('message')
        post.save()

        return Response({'post_id' : post_id}, status=status.HTTP_200_OK)

class IndexView(View):
    template_name = 'index.html'
    def get(self, request):
        losts = Post.objects.filter(type='lost')
        founds = Post.objects.filter(type='found')
        active = len(founds.filter(is_active=True))

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

        if request.user.is_authenticated:
            if request.user != post.user: # ถ้าล็อกอินและเข้าไปหน้าแก้ไขโพสต์ที่ตัวเองไม่ได้สร้าง
                return redirect('index')
        elif post.key == None: # ถ้าไม่ได้ล็อกอินและเข้าแก้ไขโพสต์ที่สร้างโดยคนที่ล็อกอิน
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

            if post.user == None and request.POST.get('key') != post.key:
                return render(request, self.template_name, {
                    'form' : form,
                    'post': post,
                    'pictures' : post.postpicture_set.all(),
                    'formset' : formset,
                    'anonymous' : True if post.user == None else False,
                    'key_error' : 'คีย์ไม่ถูกต้อง'
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

            return render(request, self.template_name, {
                'form' : form,
                'post': post,
                'pictures' : post.postpicture_set.all(),
                'formset' : formset,
                'anonymous' : True if post.user == None else False,
                'success' : 'แก้ไขข้อมูลโพสต์สําเร็จแล้ว'
            })
        else:
            return render(request, self.template_name, {
                'form' : form,
                'post': post,
                'pictures' : post.postpicture_set.all(),
                'formset' : formset,
                'anonymous' : True if post.user == None else False,
            })



def delete_view(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('my_posts')
