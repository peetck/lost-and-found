from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create/', views.CreateView.as_view(), name='create'),
    path('detail/<int:post_id>/', views.DetailView.as_view(), name='detail')
]
