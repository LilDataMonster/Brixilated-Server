import pandas as pd
from lego.models import LegoPiece
from django.core.management.base import OutputWrapper


def load_lego_pieces_csv(csv_file: str, log: OutputWrapper = None) -> bool:
    populate_pieces = lambda row: LegoPiece.objects.create(**row)

    df = pd.read_csv(csv_file,
                     header=None,
                     names=['part_number', 'name', 'category', 'description'])

    # replace nan in description with blank string
    df['description'] = df['description'].fillna('')

    # populate database
    res_df = df.apply(populate_pieces, 1)

    if log:
        log.write(f"Loaded {res_df.shape[0]} Lego Pieces into the Database")
    return True


def load_lego_set_csv(csv_file: str, log: OutputWrapper = None) -> bool:

    df = pd.read_csv(csv_file,
                     header=None,
                     names=['part_number', 'name', 'category', 'description'])

    if log:
        log.write(f"Loaded {res_df.shape[0]} Lego Pieces into the Database")

    return True