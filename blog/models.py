from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=260)
    short_description = models.CharField(max_length=320)
    description = RichTextField(blank=True, null=True)
    #description = models.TextField()
    image = models.ImageField(null=True, blank=True, upload_to="images")
    is_posted = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('post-detail', args=[str(self.pk)])

    def __str__(self):
        return self.title


class Comment(models.Model):
    username = models.CharField(max_length=120, null=True, blank=True)
    text = models.TextField()
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)

    def __str__(self):
        return self.text
