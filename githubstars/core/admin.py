from django.contrib import admin

from core.models import GithubRepo


class GithubRepoAdmin(admin.ModelAdmin):
    list_filter = ('user',)


admin.site.register(GithubRepo, GithubRepoAdmin)
