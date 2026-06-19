from django.contrib.staticfiles.management.commands.runserver import (
    Command as RunserverCommand,
)


class Command(RunserverCommand):
    help = 'Starts the development server without checking database migrations.'

    def check_migrations(self):
        pass
