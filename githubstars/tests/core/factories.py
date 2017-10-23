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
