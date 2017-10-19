from django.conf import settings
from django.db import models


class GithubRepo(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    repo_id = models.CharField(max_length=100)
    name = models.CharField(max_length=250)
    url = models.URLField()
    language = models.CharField(max_length=100)
