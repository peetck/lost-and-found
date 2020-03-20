from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'), # signup
    path('login/', views.login_view, name='login'), # login
    path('logout/', views.logout_view, name='logout'), # logout
]