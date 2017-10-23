from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models
from urllib.parse import urlparse


class RepoManager(models.Manager):
    def search_tag(self, tag):
        return self.get_queryset().filter(
            tags__contains=[tag]).distinct('url')

    def search_tag_like(self, tag):
        tag = '%%%s%%' % tag
        query = '''
        SELECT id
        FROM (
            SELECT id, unnest(tags) tag
                FROM core_githubrepo) x
                WHERE tag LIKE %s;
        '''
        ids = [res.id for res in self.get_queryset().raw(query, [tag])]
        return self.get_queryset().filter(
            id__in=ids).distinct('url')


class GithubRepo(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    repo_id = models.CharField(max_length=100)
    name = models.CharField(max_length=250)
    url = models.URLField()
    language = models.CharField(max_length=100)
    tags = ArrayField(models.CharField(max_length=100, blank=True), null=True)

    objects = RepoManager()

    def clean(self):
        if len(self.tags) != len(set(self.tags)):
            raise ValidationError('Não são permitidas tags duplicadas.')

    def __str__(self):
        parts = urlparse(self.url)
        return parts.path[1:]
