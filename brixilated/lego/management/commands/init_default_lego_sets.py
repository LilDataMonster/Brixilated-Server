import os
import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    help = 'Loads the default Lego Sets into the database'

    def add_arguments(self, parser):
        default_path = os.path.join(settings.BASE_DIR, 'lego',
                                    'management', 'commands', 'default_lego_set.csv')
        parser.add_argument('--lego_set_file', nargs=1, default=default_path)

    def handle(self, *args, **options):
        try:
            df = pd.read_csv(options['lego_set_file'])
            # TODO: process lego_set_file
        except Exception as e:
            raise CommandError(f'Unable to process file: {e}')
