from django.urls import path
from .views import SignupView, LoginView, logout_view, ProfileView, MyPostView, ChangePass_view

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'), # SignupView
    path('login/', LoginView.as_view(), name='login'), # LoginView
    path('<int:user_id>/', ProfileView.as_view(), name='profile'), # ProfileView
    path('my_posts/', MyPostView.as_view(), name='my_posts'),# myposts
    path('logout/', logout_view, name='logout'), # logout
    path('Change_Password/<int:user_id>', ChangePass_view, name='Change_Password'), # Change Password
]