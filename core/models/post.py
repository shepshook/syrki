from django.db import models
import uuid
from datetime import datetime
from django.urls import reverse
from django.utils.timezone import now
from PIL import Image, ImageOps
from .profile import Profile


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    image = models.ImageField(upload_to="img")
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="post_author")
    likes = models.ManyToManyField(Profile, related_name="liked_posts")
    content = models.TextField(blank=True)
    publication_date = models.DateTimeField()

    class Meta:
        ordering = ['-publication_date']

    def __str__(self):
        return self.user

    def date_str(self):
        delta = now() - self.publication_date
        if delta.days > 365:
            return f"{int(delta.days / 365)} years ago"
        elif delta.days > 7:
            return f"{int(delta.days / 7)} weeks ago"
        elif delta.days > 0:
            return f"{int(delta.days)} days ago"
        elif delta.seconds > 3600:
            return f"{int(delta.seconds / 3600)} hours ago"
        elif delta.seconds > 60:
            return f"{int(delta.seconds / 60)} mins ago"
        else:
            return f"{int(delta.seconds)} secs ago"

    def get_url(self):
        return reverse("post-details", args=[str(self.id)])

    def get_like_url(self):
        return f"{reverse('post-details', args=[str(self.id)])}/like"

    def get_thumbnail(self):
        img = Image.open(self.image)


class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="comment_author")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="commented_post")

    content = models.TextField()
    publication_date = models.DateTimeField()

    def date_str(self):
        delta = now() - self.publication_date
        if delta.days > 365:
            return f"{int(delta.days / 365)} years ago"
        elif delta.days > 7:
            return f"{int(delta.days / 7)} weeks ago"
        elif delta.days > 0:
            return f"{int(delta.days)} days ago"
        elif delta.seconds > 3600:
            return f"{int(delta.seconds / 3600)} hours ago"
        elif delta.seconds > 60:
            return f"{int(delta.seconds / 60)} mins ago"
        else:
            return f"{int(delta.seconds)} secs ago"
