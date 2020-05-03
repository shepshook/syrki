from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.http import Http404
from django.shortcuts import render, redirect

from core.forms.profile import ProfileCreationForm
from core.models.post import Post
from core.models.profile import Profile


def user_details(request, username):
    try:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user_id=user.id)
        posts = Post.objects.filter(user_id=user.id)
    except User.DoesNotExist:
        raise Http404("User does not exists")

    return render(request, "registration/user_details.html", {"profile": profile, "posts": posts})


def user_settings(request, username):
    if request.user.is_authenticated and request.user.username == username:
        try:
            user = User.objects.get(username=username)
            profile = Profile.objects.get(user_id=user.id)
        except User.DoesNotExist:
            raise Http404("User does not exists")

        return render(request, "registration/user_settings.html", {"profile": profile})


def user_registration(request):
    if request.method == "POST":
        form = ProfileCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            #user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.save()
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect("/")
    else:
        form = ProfileCreationForm()

    return render(request, "registration/user_registration.html", {"form": form})
