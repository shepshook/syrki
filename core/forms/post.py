from django import forms
from core.models.post import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["image", "content"]


class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.TextInput)
