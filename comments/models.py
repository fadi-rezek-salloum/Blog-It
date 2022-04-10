from django.db import models

from articles.models import Article
from accounts.models import UserProfile

class Comment(models.Model):
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE)
    article = models.ForeignKey(
        'articles.Article', related_name='comments', on_delete=models.CASCADE)

    timestamp = models.DateTimeField(auto_now_add=True)
    body = models.TextField()

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.user)
