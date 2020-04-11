from django.urls import path
from .views import IndexView, CreateView, DetailView, EditPostView, delete_view

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create/', CreateView.as_view(), name='create'),
    path('detail/<int:post_id>/', DetailView.as_view(), name='detail'),
    path('edit_post/<int:post_id>/', EditPostView.as_view(), name='edit_post'),
    path('delete/<int:post_id>/', delete_view, name='post_delete')
]
