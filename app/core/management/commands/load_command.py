# core/management/commands/initialize_data.py

from django.core.management.base import BaseCommand
from core.tests.utils.load_data import LoadData

class Command(BaseCommand):
    help = 'Initialize data'

    def handle(self, *args, **kwargs):
        LoadData.initialize_data()
        self.stdout.write(self.style.SUCCESS('Data initialized successfully'))
