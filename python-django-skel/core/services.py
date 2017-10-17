import os
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


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


class GithubClient:
    pass
