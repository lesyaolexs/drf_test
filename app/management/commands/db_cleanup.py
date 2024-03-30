from django.core.management.base import BaseCommand

from app.tasks import clean_db


class Command(BaseCommand):
    help = "Database cleanup"

    def handle(self, *args, **options):
        try:
            clean_db.apply_async()
        except Exception as err:
            self.stdout.write(self.style.ERROR("Unexpected error while processing"))
            raise err
        self.stdout.write(self.style.SUCCESS("Task processed successfully"))
