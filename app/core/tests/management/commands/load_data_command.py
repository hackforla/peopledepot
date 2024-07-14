from django.core.management.base import BaseCommand

from .load_data import load_data


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        load_data()
        self.stdout.write(self.style.SUCCESS("Data initialized successfully"))
