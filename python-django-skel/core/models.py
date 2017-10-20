from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from urllib.parse import urlparse


class GithubRepo(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    repo_id = models.CharField(max_length=100)
    name = models.CharField(max_length=250)
    url = models.URLField()
    language = models.CharField(max_length=100)
    tags = ArrayField(models.CharField(max_length=100, blank=True), null=True)

    def __str__(self):
        parts = urlparse(self.url)
        return parts.path[1:]
