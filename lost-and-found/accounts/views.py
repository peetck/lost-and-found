from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm
from posts.models import Post

# Create your views here.
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login
            login(request, user)
            return redirect('index')
    else:
        form = SignupForm()
    context = {
        'form' : form
    }
    return render(request, 'signup.html', context)

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