import os
import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from lego.data.load_data import load_lego_pieces_csv


class Command(BaseCommand):
    help = 'Loads the default Lego Pieces into the database'

    def add_arguments(self, parser):
        default_path = os.path.join(settings.BASE_DIR, 'lego', 'data', 'default_lego_pieces')
        parser.add_argument('--lego_piece_dir', nargs=1, default=default_path)

    def handle(self, *args, **options):
        path = options['lego_piece_dir']
        files = os.listdir(path)
        for filename in files:
            try:
                # only process csv files
                if not filename.endswith('.csv'):
                    continue
                file_path = os.path.join(path, filename)
                self.stdout.write(f"Processing File: {file_path}", ending='... ')
                load_lego_pieces_csv(file_path, self.stdout)
            except Exception as e:
                # raise CommandError(f'Unable to process file: {e}')
                self.stdout.flush()
                self.stderr.write(f'Unable to process file: {e}')