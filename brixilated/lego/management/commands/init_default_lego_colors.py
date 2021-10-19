import os
import glob
from django.core.management.base import BaseCommand
from django.conf import settings
from lego.data.load_data import load_lego_colors_csv


class Command(BaseCommand):
    help = 'Loads the default Lego Colors into the database'

    def add_arguments(self, parser):
        default_path = glob.glob(os.path.join(settings.BASE_DIR, 'lego', 'data', '*.csv'))
        parser.add_argument('--lego_set_colors', nargs=1, default=default_path)

    def handle(self, *args, **options):
        file_path = None if len(options['lego_set_colors']) == 0 else options['lego_set_colors'][0]

        try:
            # process file
            self.stdout.write(f"Processing File: {file_path}", ending='... ')
            if not file_path:
                self.stdout.write()
            load_lego_colors_csv(file_path, False, self.stdout)

        except Exception as e:
            self.stdout.flush()
            self.stderr.write(f'Unable to process file: {e}')
