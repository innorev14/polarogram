from django.conf import settings
from django.db import models
from django.urls import reverse


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='timeline_photo/%Y/%m/%d')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked', blank=True)
    saved = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='saved', blank=FutureWarning)

    class Meta:
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('post:detail', args=[str(self.id)])




