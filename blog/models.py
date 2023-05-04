from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


User = get_user_model()


class Post(models.Model):
    BOOL = (
        (True, 'Publish'),
        (False, 'Draft'),
    )

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    heading = models.CharField(max_length=50, default='No heading')
    text = models.TextField()
    short_definition = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/',
                              blank=True,
                              null=True,
                              default='moon.png',
                              verbose_name='Load Image')
    is_published = models.BooleanField(choices=BOOL, verbose_name='Publish or Draft')
    pub_date = models.DateTimeField('date published', auto_now=True)

    def __str__(self):
        return self.heading


class Comment(models.Model):
    author = models.CharField(max_length=100, verbose_name='username')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=400)
    is_published = models.BooleanField(default=False)
    pub_date = models.DateTimeField('date published', blank=True, null=True, auto_now=True)

    def __str__(self):
        return self.text
