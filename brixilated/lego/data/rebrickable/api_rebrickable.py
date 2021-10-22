import time
from datetime import datetime
import requests
import pandas as pd
from tqdm import tqdm


class RebrickableAPI(object):

    def __init__(self, api_key: str):
        self.API_KEY = api_key

    def fetch_data(self, url: str, timeout: int = 10) -> pd.DataFrame:
        df = pd.DataFrame()
        headers = {'Authorization': f'key {self.API_KEY}'}

        # get metadata
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            data = response.json()
            num_entries = data['count']
        except Exception as e:
            print(f'Got Exception {e}')
            return None

        with tqdm(total=num_entries) as pbar:
            while True:
                try:
                    response = requests.get(url, headers=headers, timeout=timeout)
                    if not response.ok:
                        print(f'Error received: {response} retrying...')
                        time.sleep(2)
                        continue

                    data = response.json()
                    df_response = pd.json_normalize(data['results'])
                    df = df.append(df_response)

                    pbar.update(df_response.shape[0])

                    if data['next']:
                        url = data['next']
                    else:
                        if data['count'] != df.shape[0]:
                            print(f'Got {df.shape[0]} entries, expected {data["count"]} entries')
                        break
                    time.sleep(0.5) # rate limit to 1 request/sec
                except TimeoutError:
                    print('Timed Out')
        return df.reset_index(drop=True)

    def get_colors(self, write_csv: bool = True):
        url = f'https://rebrickable.com/api/v3/lego/colors/?key={API_KEY}'
        df = self.fetch_data(url)
        if df and write_csv:
            df.to_csv(f'colors_{datetime.now().strftime("%Y-%m-%d")}.csv', index=False)
        return df

    def get_parts(self, write_csv: bool = True):
        url = f'https://rebrickable.com/api/v3/lego/parts/?page_size=500'
        df = self.fetch_data(url)
        if df and write_csv:
            df.to_csv(f'parts_{datetime.now().strftime("%Y-%m-%d")}.csv', index=False)
        return df


API_KEY = 'b6e77fd23f84e024757f8ecff3749d78'
api = RebrickableAPI(API_KEY)
api.get_parts()
