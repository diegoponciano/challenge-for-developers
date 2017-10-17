from core.services import get_repos, GithubClient
from model_mommy import random_gen


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


def test_github_client():
    cli = GithubClient()
    assert cli


def test_sync():
    pass
