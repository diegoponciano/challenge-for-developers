import pytest
from django.db import IntegrityError
from model_mommy import mommy, random_gen

from core.models import GithubRepo


@pytest.mark.django_db
def test_invalid_model_creation():
    repo = GithubRepo()
    with pytest.raises(IntegrityError):
        repo.save()


@pytest.mark.django_db
def test_model_creation(user):
    repo = GithubRepo(
        user=user,
        repo_id=random_gen.gen_integer())
    repo.save()

    assert repo.id


@pytest.mark.django_db
def test_model_str():
    gh_repo = mommy.make(
        GithubRepo,
        url='http://github.com/gravity/zero')
    assert str(gh_repo) == 'gravity/zero'

    gh_repo = mommy.make(
        GithubRepo,
        url='https://github.com/gravity/zero')
    assert str(gh_repo) == 'gravity/zero'


@pytest.mark.django_db
def test_model_tags():
    gh_repo = mommy.make(GithubRepo)
    gh_repo.tags = ['javascript', 'js', 'node']
    gh_repo.save()

    gh_repo = GithubRepo.objects.get(pk=gh_repo.pk)

    assert len(gh_repo.tags) == 3
    assert 'javascript' in gh_repo.tags
