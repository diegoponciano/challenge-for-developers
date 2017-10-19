import os
from django.contrib.auth import get_user_model
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

from .models import GithubRepo


def query_repos(user, pagesize=100, cursor=None):
    cursor = 'after: "%s"' % cursor if cursor else ''
    query = '''
        query {
            user(login: "%s") {
                starredRepositories(first: %s, %s) {
                    edges {
                        node {
                            id
                            name
                            url
                            languages(first: 10) {
                                edges {
                                    node {
                                        name
                                    }
                                }
                            }
                        }
                        cursor
                    }
                    pageInfo {
                        hasNextPage
                        hasPreviousPage
                        endCursor
                    }
                }
            }
        }''' % (user, pagesize, cursor)
    headers = {'Authorization': 'bearer %s' % os.getenv('GITHUB_API_TOKEN')}
    url = 'https://api.github.com/graphql'
    transport = RequestsHTTPTransport(url, headers=headers, use_json=True)
    client = Client(transport=transport)
    resp = client.execute(gql(query))
    repositories = resp.get('user').get('starredRepositories')
    return repositories


def get_repos(user):
    repos = []
    has_next = True
    cursor = None
    while has_next:
        resp = query_repos(user, cursor=cursor)
        repos.extend(resp['edges'])
        cursor = resp['pageInfo']['endCursor']
        has_next = resp['pageInfo']['hasNextPage']
    return repos


def get_language(repo):
    try:
        return repo['node']['languages']['edges'][0]['node']['name']
    except IndexError:
        return ''


class GithubClient:
    def __init__(self, username):
        self.username = username

    def sync_repos(self):
        repos = get_repos(self.username)
        if repos:
            user = get_user_model().objects.get(username=self.username)
            for repo in repos:
                GithubRepo.objects.create(
                    user=user,
                    repo_id=repo['node']['id'],
                    name=repo['node']['name'],
                    url=repo['node']['url'],
                    language=get_language(repo)
                )
