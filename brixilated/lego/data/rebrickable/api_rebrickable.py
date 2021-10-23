import time
from datetime import datetime
import requests
import pandas as pd
from tqdm import tqdm

from django.core.management.base import OutputWrapper


class RebrickableAPI(object):

    def __init__(self, api_key: str, log: OutputWrapper = None):
        self.API_KEY = api_key
        self.date_retrieved = datetime.now().strftime("%Y-%m-%d")
        self.log = log

    def fetch_data(self, url: str, timeout: int = 10) -> pd.DataFrame:
        df = pd.DataFrame()
        headers = {'Authorization': f'key {self.API_KEY}'}

        # get metadata
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            data = response.json()
            num_entries = data['count']
        except Exception as e:
            if self.log:
                self.log.write(f'Got Exception {e}')
            return None

        # fetch data
        with tqdm(total=num_entries) as pbar:
            while True:
                try:
                    response = requests.get(url, headers=headers, timeout=timeout)
                    if not response.ok:
                        if self.log:
                            self.log.write(f'Error received: {response} retrying...')
                        time.sleep(2)
                        continue

                    data = response.json()
                    df_response = pd.json_normalize(data['results'])
                    df = df.append(df_response)

                    pbar.update(df_response.shape[0])

                    if data['next']:
                        url = data['next']
                    else:
                        if data['count'] != df.shape[0] and self.log:
                            self.log.write(f'Got {df.shape[0]} entries, expected {data["count"]} entries')
                        break
                    time.sleep(0.5) # rate limit to 1 request/sec
                except TimeoutError:
                    if self.log:
                        self.log.write('Timed Out')
        return df.reset_index(drop=True)

    def get_colors(self, write_csv: bool = True):
        url = f'https://rebrickable.com/api/v3/lego/colors/?page_size=500'
        df = self.fetch_data(url)
        if df is not None and write_csv:
            csv_path = f'colors_{self.date_retrieved}.csv'
            df.to_csv(csv_path, index=False)
            if self.log:
                self.log.write(f'Saved colors to: {csv_path}')
        return df

    def get_parts(self, write_csv: bool = True):
        url = f'https://rebrickable.com/api/v3/lego/parts/?page_size=500'
        df = self.fetch_data(url)
        if df is not None and write_csv:
            csv_path = f'parts_{self.date_retrieved}.csv'
            df.to_csv(csv_path, index=False)
            if self.log:
                self.log.write(f'Saved parts to: {csv_path}')
        return df

    def get_part_categories(self, write_csv: bool = True):
        url = f'https://rebrickable.com/api/v3/lego/part_categories/?page_size=500'
        df = self.fetch_data(url)
        if df is not None and write_csv:
            csv_path = f'part_categories_{self.date_retrieved}.csv'
            df.to_csv(csv_path, index=False)
            if self.log:
                self.log.write(f'Saved part categories to: {csv_path}')
        return df
