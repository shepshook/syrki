from django.urls import path

from core.views import post

urlpatterns = [
    path("", post.feed, name="feed"),
    path("post/<uuid:pk>", post.post_details, name="post-details"),
    path("post/<uuid:pk>/like", post.post_like, name="post-like"),
    path("post/create", post.create_post, name="create-post"),
]