import os
import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    help = 'Loads the default Lego Sets into the database'

    def add_arguments(self, parser):
        default_path = os.path.join(settings.BASE_DIR, 'lego', 'data', 'default_lego_sets')
        parser.add_argument('--lego_set_dir', nargs=1, default=default_path)

    def handle(self, *args, **options):
        try:
            # TODO: process lego_set_file
            path_dir = os.listdir(options['lego_set_dir'])
            for filename in path_dir:
                # only process csv files
                if not filename.endswith('.csv'):
                    continue
                df = pd.read_csv(os.path.join(path_dir, filename))
        except Exception as e:
            raise CommandError(f'Unable to process file: {e}')
