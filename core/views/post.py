from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.utils.timezone import now
import logging

from core.forms.post import PostForm, CommentForm
from core.models.post import Post, Comment
from core.models.profile import Profile


def feed(request):
    return render(request, "feed.html", {"posts_list": Post.objects.all()})


def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = Post()
            post.publication_date = now()
            post.user_id = Profile.objects.filter(user_id=request.user.id).first().id
            post.image = request.FILES["image"]
            post.content = form.cleaned_data.get("content")
            post.save()
            logging.info("New post of user %s created", request.user.username)
            return HttpResponseRedirect("/")
    else:
        form = PostForm()
    return render(request, "create_post.html", {"form": form})


def post_details(request, pk):
    try:
        post = Post.objects.get(id=pk)
        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = Comment()
                comment.user_id = Profile.objects.filter(user_id=request.user.id).first().id
                comment.publication_date = now()
                comment.content = form.cleaned_data.get("content")
                comment.post = post
                comment.save()
                logging.info("New comment of user %s posted to post %s", request.user.username, post.id)

        form = CommentForm()
        comments = Comment.objects.filter(post_id=pk)

    except Post.DoesNotExist:
        raise Http404("Post does not exists")

    return render(request, "post_details.html", {"post": post, "form": form, "comments": comments})


def post_like(request, pk):
    post = Post.objects.get(id=pk)
    if request.user.is_authenticated:
        user = Profile.objects.get(user=request.user)
        if user in post.likes.all():
            post.likes.remove(user)
            logging.info("User %s disliked post %s", request.user.username, post.id)
        else:
            post.likes.add(user)
            logging.info("User %s liked post %s", request.user.username, post.id)

    return HttpResponseRedirect(post.get_url())
