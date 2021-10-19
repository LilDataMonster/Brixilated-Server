import numpy as np
import pandas as pd
from functools import partial
from lego.models import LegoPiece, LegoPieces, LegoSet, LegoColor
from django.core.management.base import OutputWrapper

from .colors import fetch_colors


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
        log.write(f'Loaded {res_df.shape[0]} Lego Pieces into the Database')
    return True


def populate_set(row: pd.Series, lego_set: LegoSet, log: OutputWrapper = None) -> LegoPieces:
    piece, created = LegoPiece.objects.get_or_create(part_number=row['part_number'])
    if created and log:
        log.write(f'Lego Piece with Part Number: {row["part_number"]} not found in database... New Entry Created.')

    pieces = LegoPieces.objects.create(lego_set=lego_set,
                                       lego_piece=piece,
                                       hex_color=int(row["hex_color"], 0),
                                       quantity=row["quantity"])
    return pieces


def load_lego_set_csv(csv_file: str, log: OutputWrapper = None) -> bool:
    # create set
    df_set = pd.read_csv(csv_file,
                         header=None,
                         nrows=1,
                         names=['name', 'is_complete_set', 'description'])

    # replace nan in description with blank string
    df_set['description'] = df_set['description'].fillna('')

    # lego_set = df_set.apply(populate_set, 1)[0]
    lego_set = LegoSet.objects.create(**df_set.iloc[0])
    if log:
        log.write(f'\nLego set created: {lego_set}')

    # create pieces
    df_pieces = pd.read_csv(csv_file,
                            header=None,
                            skiprows=1,
                            names=['part_number', 'quantity', 'hex_color'])

    populate_lego_set = partial(populate_set, lego_set=lego_set, log=log)
    res_df = df_pieces.apply(populate_lego_set, 1)

    if log:
        num_parts = res_df.apply(lambda x: x.quantity).sum()
        log.write('=============================================')
        log.write(f'Loaded Lego Set into database:')
        log.write(f'Lego Set Name: {lego_set.name}')
        log.write(f'Lego Set Description: {lego_set.description}')
        log.write(f'Total Number of Pieces: {num_parts}')
        log.write(f'Unique Number of Pieces: {res_df.shape[0]}')
        log.write('=============================================')

    return True


def load_lego_colors_csv(csv_file: str, fetch_data: bool = False, log: OutputWrapper = None) -> bool:

    if csv_file is None:
        fetch_data = True

    # get colors
    df_colors = fetch_colors(log) if fetch_data else pd.read_csv(csv_file)

    # rename headers
    df_colors.rename(columns={
        "Material": "material",
        "LEGO ID": "lego_id",
        "LEGO Name (*=unconfirmed)": "lego_name",
        "BL ID": "bl_id",
        "BL Name": "bl_name",
        "BO Name": "bo_name",
        "LDraw ID": "ldraw_id",
        "LDraw Name": "ldraw_name",
        "Peeron Name": "peeron_name",
        "Other": "other",
        "Years Active Start": "year_start",
        "Years Active End": "year_end",
        "Notes": "notes",
        "Hex": "hex_code",
        "C": "cyan",
        "M": "magenta",
        "Y": "yellow",
        "K": "black",
        "Pantone": "pantone"
    }, inplace=True)

    headers = ['material', 'lego_id', 'lego_name', 'bl_id', 'bl_name', 'bo_name',
               'ldraw_id', 'ldraw_name', 'peeron_name', 'other', 'year_start', 'year_end',
               'notes', 'hex_code', 'cyan', 'magenta', 'yellow', 'black', 'pantone']
    df_colors = df_colors[headers]

    # replace NaN with None
    df_colors = df_colors.fillna(np.nan).replace([np.nan, ''], [None, None])
    df_colors['year_end'] = df_colors['year_end'].replace(['Present', '?'], [None, None])
    df_colors['year_start'] = df_colors['year_start'].replace(['Present', '?'], [None, None])

    # translate material to code
    df_colors['material'] = df_colors['material'].apply(lambda x: LegoColor.LegoColorCategory[x.upper()])

    # create colors
    populate_colors = lambda row: LegoColor.objects.create(**row)
    lego_colors = df_colors.apply(populate_colors, 1)
    if log:
        log.write('\n=============================================')
        log.write(f'Loaded Lego Colors into database:')
        log.write(f'Loaded lego Colors: {lego_colors.shape[0]}')
        log.write('=============================================')

    return True
