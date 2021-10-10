import os
from django.core.management.base import BaseCommand
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

                # get file path
                file_path = os.path.join(path, filename)

                # process file
                self.stdout.write(f"Processing File: {file_path}", ending='... ')
                load_lego_pieces_csv(file_path, self.stdout)
            except Exception as e:
                self.stdout.flush()
                self.stderr.write(f'Unable to process file: {e}')
