from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from core.services import GithubClient


class Command(BaseCommand):
    help = 'Syncs starred repositories from Github'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)

    def handle(self, *args, **options):
        username = options['username']
        if not get_user_model().objects.filter(username=username).exists():
            raise CommandError(
                'Usuário "%s" ainda não existe. Crie um com o comando "createsuperuser".'
                % username)
        cli = GithubClient(username)
        cli.sync_repos()
        self.stdout.write(self.style.SUCCESS(
            'Repositórios do "%s" sincronizados com sucesso.' % username))
