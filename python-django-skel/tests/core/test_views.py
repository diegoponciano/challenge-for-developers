import pytest
from model_mommy import mommy

from core.models import GithubRepo


def test_home(client):
    response = client.get('/')
    assert b'tags' in response.content


def test_search(client):
    response = client.get('/busca')
    assert response.status_code == 200


@pytest.mark.django_db
def test_search_results(client):
    mommy.make(GithubRepo, url='https://github.com/asd/qwe', tags=['elixir'])
    mommy.make(GithubRepo, url='https://github.com/zxc/vbn', tags=['groovy'])

    response = client.get('/busca?q=elixir')
    assert b'asd/qwe' in response.content
    assert b'zxc/vbn' not in response.content

    response = client.get('/busca?q=groovy')
    assert b'asd/qwe' not in response.content
    assert b'zxc/vbn' in response.content
