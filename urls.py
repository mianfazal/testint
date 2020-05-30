# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.urls import path
from .views import (
                    PostListView,
                    PostDetailView,
                    PostCreateView,
                    PostUpdateView,
                    PostDeleteView,
                    UserPostListView ) # same as importing function name now we include class
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'), #.as_view() find html page in PostListView automatically and i tell in class already
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'), #<int:pk> go other html page with primary key of that post pk comes when clicked on current post and passd to this path in url
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),

    path('livetryon/', views.livetryon, name='live-tryon'),
    path('imagetryon/', views.imagetryon, name='image-tryon'),
    path('about/', views.about, name='blog-about'),
]
