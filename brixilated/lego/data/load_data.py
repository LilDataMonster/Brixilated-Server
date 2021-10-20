import os
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
    custom_piece = row['element_id'] is None
    color = None
    if not custom_piece:
        # get or create color
        color_headers = ['bl_color_id', 'bl_color_name', 'ldraw_color_id', 'material']
        df_colors = row[color_headers]
        color, created = LegoColor.objects.get_or_create(**df_colors)
        if created and log:
            log.write(f'Lego Color: {row["bl_color_name"]}, LDrawID: {row["ldraw_color_id"]}'
                      f' not found in database... New Entry Created.')

    # get or create piece
    piece_headers = ['part_name', 'weight', 'ldraw_id', 'bl_item_no']
    df_piece = row[piece_headers]
    piece, created = LegoPiece.objects.get_or_create(custom_piece=custom_piece, **df_piece)
    if created and log:
        log.write(f'Lego Piece: {row["part_name"]} with Part Number: {row["element_id"]} '
                  f'and LDraw ID: {row["ldraw_id"]} not found in database... New Entry Created.')

    pieces = LegoPieces.objects.create(lego_set=lego_set,
                                       lego_piece=piece,
                                       lego_color=color,
                                       element_id=row['element_id'],
                                       quantity=row['quantity'])
    return pieces


def load_lego_set_csv(csv_file: str, log: OutputWrapper = None) -> bool:
    # create set
    lego_set_name = os.path.splitext(os.path.basename(csv_file))[0].replace('_Partlist', '')
    lego_set = LegoSet.objects.create(name=lego_set_name,
                                      is_complete_set=True)

    if log:
        log.write(f'\nLego set created: {lego_set}')

    # populate set
    df_set = pd.read_csv(csv_file, engine='python', skipfooter=3)
    df_set.rename(columns={
        "BLItemNo": "bl_item_no",
        "ElementId": "element_id",
        "LdrawId": "ldraw_id",
        "PartName": "part_name",
        "BLColorId": "bl_color_id",
        "LDrawColorId": "ldraw_color_id",
        "ColorName": "bl_color_name",
        "ColorCategory": "material",
        "Qty": "quantity",
        "Weight": "weight"
    }, inplace=True)

    # translate material to code
    df_set['material'] = df_set['material'].apply(
        lambda x: LegoColor.LegoColorCategory[x.replace(' Colors', '').upper()])

    # replace NaN with None
    df_set = df_set.fillna(np.nan).replace([np.nan, ''], [None, None])

    populate_lego_set = partial(populate_set, lego_set=lego_set, log=log)
    res_df = df_set.apply(populate_lego_set, 1)

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
        "LEGO Name (*=unconfirmed)": "name",
        "BL ID": "bl_color_id",
        "BL Name": "bl_color_name",
        "BO Name": "bo_color_name",
        "LDraw ID": "ldraw_color_id",
        "LDraw Name": "ldraw_color_name",
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

    headers = ['material', 'lego_id', 'name', 'bl_color_id', 'bl_color_name', 'bo_color_name',
               'ldraw_color_id', 'ldraw_color_name', 'peeron_name', 'other', 'year_start', 'year_end',
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
