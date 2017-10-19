import pytest
from model_mommy import random_gen

import core
from core.models import GithubRepo
from core.services import get_language, get_repos, GithubClient


def random_repos(number):
    repos = []
    for _ in range(number):
        repos.append({
            'node': {
                'id': random_gen.gen_string(12),
                'languages': {'edges': [{'node': {'name': 'Shell'}}]},
                'name': random_gen.gen_string(8),
                'url': random_gen.gen_url()
            }
        })
    return repos


def test_get_repos(mocker):
    mocker.patch('core.services.query_repos', return_value={
        'edges': random_repos(10),
        'cursor': random_gen.gen_string(12),
        'pageInfo': {
            'endCursor': random_gen.gen_string(12),
            'hasNextPage': False
        }
    })
    repos = get_repos('diego')
    assert len(repos) == 10


def test_get_paginated_repos(mocker):
    mocker.patch('core.services.query_repos', side_effect=[{
        'edges': random_repos(50),
        'cursor': random_gen.gen_string(12),
        'pageInfo': {
            'endCursor': random_gen.gen_string(12),
            'hasNextPage': True
        }
    }, {
        'edges': random_repos(10),
        'cursor': random_gen.gen_string(12),
        'pageInfo': {
            'endCursor': random_gen.gen_string(12),
            'hasNextPage': False
        }
    }])
    repos = get_repos('diego')
    assert len(repos) == 60


def test_get_real_repos():
    repos = get_repos('diegoponciano')
    assert len(repos) > 100


def test_get_language_empty():
    repo = {'node': {
        'languages': {'edges': []}}
    }
    lang = get_language(repo)
    assert lang == ''


def test_get_language():
    repo = {'node': {
        'languages': {'edges': [{'node': {'name': 'Javascript'}}]}}
    }
    lang = get_language(repo)
    assert lang == 'Javascript'


def test_github_client_requires_username():
    with pytest.raises(TypeError):
        GithubClient()


def test_github_client():
    cli = GithubClient('diegoponciano')
    assert cli


def test_sync_call(mocker):
    mocker.patch('core.services.get_repos', return_value=[])

    cli = GithubClient('randomweirdo')
    cli.sync_repos()
    core.services.get_repos.assert_called_once_with('randomweirdo')


@pytest.mark.django_db
def test_sync_call_with_django_user(mocker, user):
    mocker.patch('core.services.get_repos', return_value=[])

    cli = GithubClient(user.username)
    cli.sync_repos()
    core.services.get_repos.assert_called_once_with('diegoponciano')


@pytest.mark.django_db
def test_sync_create_repo_instances(mocker, user):
    GithubRepo.objects.all().delete()
    repos = {
        'edges': random_repos(10),
        'cursor': random_gen.gen_string(12),
        'pageInfo': {
            'endCursor': random_gen.gen_string(12),
            'hasNextPage': False
        }
    }
    mocker.patch('core.services.query_repos', return_value=repos)

    cli = GithubClient(user.username)
    cli.sync_repos()

    assert GithubRepo.objects.filter(user=user).count() == 10
    assert GithubRepo.objects.filter(
        repo_id=repos['edges'][0]['node']['id']).exists()
    assert GithubRepo.objects.filter(
        name=repos['edges'][0]['node']['name']).exists()
    assert GithubRepo.objects.filter(
        url=repos['edges'][0]['node']['url']).exists()
