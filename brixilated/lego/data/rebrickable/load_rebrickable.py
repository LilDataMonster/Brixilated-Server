import requests
import gzip
import pandas as pd
from io import StringIO


def download_decompress_csv(url: str) -> pd.DataFrame:
    r = requests.get(url)
    bytes = gzip.decompress(r.content)
    data = StringIO(str(bytes, 'utf-8'))
    df = pd.read_csv(data)
    return df


def download_parts_db():
    url = 'https://cdn.rebrickable.com/media/downloads/parts.csv.gz'
    df = download_decompress_csv(url)
    # print(gzip.decompress(r.content))


def download_colors_df() -> pd.DataFrame:
    url = 'https://cdn.rebrickable.com/media/downloads/colors.csv.gz'
    df = download_decompress_csv(url)
    print(df)


download_parts_db()
download_colors_df()