from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm
from .models import Faculty, UserProfile
from posts.models import Post
from django.contrib.auth.models import User
from django.views import View

# Create your views here.
class SignupView(View):
    context = {}
    template_name = 'signup.html'
    def get(self, request):
        form = SignupForm()

        self.context['form'] = form
        self.context['facultys'] = Faculty.objects.all()

        return render(request, self.template_name, self.context)

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            faculty = Faculty.objects.get(
                id=request.POST.get('faculty')
            )

            userprofile = UserProfile.objects.create(
                user=user,
                faculty=faculty
            )
            # login
            login(request, user)
            return redirect('index')
        else:
            self.context['form'] = form
            self.context['facultys'] = Faculty.objects.all()
            return render(request, self.template_name, self.context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            """ next_url = request.POST.get('next_url')
            if next_url != 'None':
                return redirect(next_url)
            else: """
            return redirect('index')
        context['error'] = 'ชื่อผู้ใช้งานหรือรหัสผ่านไม่ถูกต้อง'

    next_url = request.GET.get('next') # if have next_url send it to save in input:hidden
    context['next_url'] = next_url
    return render(request, 'login.html', context)

def logout_view(request):
    logout(request)
    return redirect('index')

def my_posts_view(request):
    if request.user.is_authenticated:
        posts = Post.objects.filter(user=request.user)
    else:
        posts = "key"
    context = {
        'posts' : posts
    }
    return render(request, 'my_posts.html', context)


def profile_view(request, user_id):
    user = User.objects.get(id=user_id)
    context = {
        'user' : user
    }
    return render(request, 'profile.html', context)