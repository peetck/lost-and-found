from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm
from .models import Faculty, UserProfile
from posts.models import Post
from chats.models import Chat
from django.contrib.auth.models import User
from django.views import View

# Create your views here.
class SignupView(View):
    template_name = 'signup.html'
    def get(self, request):
        form = SignupForm()
        return render(request, self.template_name, {
            'form' : form,
            'facultys' : Faculty.objects.all()
        })

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            faculty = Faculty.objects.get(
                id=request.POST.get('faculty')
            )

            try:
                picture = request.FILES['picture']
            except:
                picture = None

            userprofile = UserProfile.objects.create(
                user=user,
                faculty=faculty
            )

            if picture != None:
                userprofile.avatar = picture
                userprofile.save()

            Chat.objects.create(
                user=user
            )
            # login
            login(request, user)
            return redirect('index')
        else:
            return render(request, self.template_name, {
                'form' : form,
                'facultys' : Faculty.objects.all()
            })

class LoginView(View):
    template_name = 'login.html'
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        next_url = request.GET.get('next') # if have next send it to save in input:hidden
        return render(request, 'login.html', {
            'next_url' : next_url
        })

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        next_url = request.POST.get('next_url')
        if user:
            login(request, user)
            if next_url != 'None':
                return redirect(next_url)
            else:
                return redirect('index')

        return render(request, 'login.html', {
            'next_url' : next_url,
            'error' : 'ชื่อผู้ใช้งานหรือรหัสผ่านไม่ถูกต้อง'
        })


class MyPostView(View):
    template_name = 'my_posts.html'

    def get(self, request):
        if request.user.is_authenticated:
            posts = Post.objects.filter(user=request.user)
        else:
            posts = "key"
        return render(request, self.template_name, {
            'posts' : posts
        })

    def post(self, request):
        key = request.POST.get('key')
        try:
            posts = Post.objects.get(key=key)
        except:
            posts = []

        return render(request, self.template_name, {
            'posts' : posts
        })

class ProfileView(View):
    template_name = 'profile.html'

    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        context = {
            'user' : user
        }
        return render(request, self.template_name, context)


def logout_view(request):
    logout(request)
    return redirect('index')

