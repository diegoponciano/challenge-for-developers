import sys
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.hashers import make_password
from getpass import getpass


User = get_user_model()


class Command(BaseCommand):
    help = 'Creates user'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('username')
        parser.add_argument('password')
        parser.add_argument('email')

    def _ask_password(self):
        password = None
        try:
            while True:
                if password is None:
                    password = getpass('Password: ')
                    password2 = getpass('Password (again): ')
                    if password != password2:
                        sys.stderr.write(
                            "Error: Your passwords didn't match.\n")
                        password = None
                        continue
                if password.strip() == '':
                    sys.stderr.write("Error: Blank passwords aren't allowed.\n")
                    password = None
                    continue
                break
        except KeyboardInterrupt:
            raise CommandError('Cancelled.')
        return password

    def handle(self, *args, **options):
        # password = self._ask_password()
        u = User.objects.create_user(
            username=options['username'],
            email=options['email'],
            password=make_password(options['password']),
            is_staff=True, is_superuser=True)
        u.save()
        self.stdout.write(self.style.SUCCESS(
            'Usuário "%s" criado com sucesso.' % options['username']))
