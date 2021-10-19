import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

from django.conf import settings
from django.core.management.base import OutputWrapper


def fetch_colors(log: OutputWrapper = None) -> pd.DataFrame:
    url = 'http://ryanhowerter.net/colors.php'

    if log:
        log.write(f'Fetching colors from {url}')

    # provide headers to avoid security mod
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
    r = requests.get(url, headers=headers)

    if log:
        log.write('Parsing Lego Colors')

    # setup parser
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('table', attrs={'class': 'table-striped'})

    # parse table header
    table_header = table.find('thead')
    data_header = table_header.find_all('tr')[0].find_all('th')
    data_header = [ele.text.strip() for ele in data_header]

    # parse table body
    data = []
    table_body = table.find('tbody')
    body_rows = table_body.find_all('tr')
    for row in body_rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append(cols)

    # fix years header to correctly align columns
    year_start_idx = data_header.index('Years Active (inclusive)')
    data_header[year_start_idx] = 'Years Active Start'
    data_header.insert(year_start_idx+1, 'Years Active End')

    timestamp = f"{datetime.datetime.now():%Y-%m-%d}"
    file = os.path.join(settings.BASE_DIR, 'lego', 'data', f'{timestamp}_lego_colors.csv')
    if log:
        log.write(f'Writing default lego colors to {file}', ending='... ')
    df = pd.DataFrame(data, columns=data_header)
    df.to_csv(file, index=False)
    return df
