from django.contrib import admin

from core.models import GithubRepo


class GithubRepoAdmin(admin.ModelAdmin):
    pass


admin.site.register(GithubRepo, GithubRepoAdmin)
