import pytest
from core.models import GithubRepo
from django.db import IntegrityError
from model_mommy import random_gen


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
