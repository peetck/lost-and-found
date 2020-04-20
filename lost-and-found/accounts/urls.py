from django.urls import path
from .views import SignupView, LoginView, logout_view, ProfileView, MyPostView, ChangePasswordView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'), # SignupView
    path('login/', LoginView.as_view(), name='login'), # LoginView
    path('<int:user_id>/', ProfileView.as_view(), name='profile'), # ProfileView
    path('my_posts/', MyPostView.as_view(), name='my_posts'),# myposts
    path('logout/', logout_view, name='logout'), # logout
    path('change_password/', ChangePasswordView.as_view(), name='change_password'), # Change Password
]