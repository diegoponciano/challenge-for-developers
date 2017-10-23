from django.shortcuts import render
from core.models import GithubRepo


def home(request):
    return render(request, 'home.html')


def search(request):
    query = request.GET.get('q')
    if query:
        results = GithubRepo.objects.search_tag_like(query)
    else:
        results = GithubRepo.objects.none()
    return render(request, 'search.html', {'results': results})
