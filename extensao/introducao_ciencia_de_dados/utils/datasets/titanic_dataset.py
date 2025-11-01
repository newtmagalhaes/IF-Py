from os import path

import pandas as pd
import requests

from .common import DOWNLOAD_DIR

_TITANIC_URL = 'https://raw.githubusercontent.com/datasciencedojo/datasets/refs/heads/master/titanic.csv'
_FILENAME = 'titanic.csv'


def load_titanic() -> pd.DataFrame:
    cache_file = DOWNLOAD_DIR / _FILENAME
    if not path.exists(cache_file):
        response = requests.get(_TITANIC_URL, timeout=(10, 10))
        response.raise_for_status()
        with open(cache_file, 'wb') as titanic_cache:
            titanic_cache.write(response.content)

    with open(cache_file, 'rb') as titanic_cache:
        return pd.read_csv(titanic_cache)


if __name__ == '__main__':
    titanic = load_titanic()
    print(titanic.head())
