from django.db import models
from django.urls import reverse

from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager

from accounts.models import UserProfile


class Article(models.Model):
    title = models.CharField(max_length=100)
    text = RichTextUploadingField(verbose_name='text', blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to="images/")
    timestamp = models.DateTimeField(auto_now_add=True)

    views = models.IntegerField(default=0)

    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE)
    tags = TaggableManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article-detail', kwargs={
            'pk': self.pk
        })

    def get_update_url(self):
        return reverse('article-update', kwargs={
            'pk': self.pk
        })

    def get_delete_url(self):
        return reverse('article-delete', kwargs={
            'pk': self.pk
        })

    def yearpublished(self):
        return self.timestamp.strftime('%Y')

    def monthpublished(self):
        return self.timestamp.strftime('%m')

    def daypublished(self):
        return self.timestamp.strftime('%d')
