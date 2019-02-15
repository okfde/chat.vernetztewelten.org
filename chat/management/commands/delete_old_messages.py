from django.core.management.base import BaseCommand
from ...models import delete_old_messages


class Command(BaseCommand):
    help = 'Lösche alte Nachrichten'

    def handle(self, *args, **options):
        delete_old_messages()
        self.stdout.write(
            self.style.SUCCESS('Alle alten Nachrichten gelöscht.')
        )
