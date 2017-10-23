import pytest
from model_mommy import mommy

from core.models import GithubRepo


def setup():
    GithubRepo.objects.all().delete()

    for i in range(10):
        tags = None
        if i < 4:
            tags = ['python']
        elif i < 8:
            tags = ['java', 'javascript']
        else:
            tags = ['python', 'javascript']

        mommy.make(GithubRepo, tags=tags)


@pytest.mark.django_db
def test_search_exact_tags():
    assert GithubRepo.objects.search_tag('ruby').count() == 0
    assert GithubRepo.objects.search_tag('java').count() == 4
    assert GithubRepo.objects.search_tag('javascript').count() == 6


@pytest.mark.django_db
def test_search_similar_tags():
    assert GithubRepo.objects.search_tag_like('ruby').count() == 0
    assert GithubRepo.objects.search_tag_like('java').count() == 6  # includes javascript
    assert GithubRepo.objects.search_tag_like('javascript').count() == 6
