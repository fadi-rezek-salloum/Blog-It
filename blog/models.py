from django.db import models

from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    subject = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.subject
