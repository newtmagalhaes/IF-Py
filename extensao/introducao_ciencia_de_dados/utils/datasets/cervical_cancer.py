from os.path import exists
from zipfile import ZipFile

import pandas as pd
import requests

from .common import DOWNLOAD_DIR


_CERVICAL_CANCER_URL = 'https://archive.ics.uci.edu/static/public/383/cervical+cancer+risk+factors.zip'
_FILENAME = 'risk_factors_cervical_cancer.csv'


def load_cervical_cancer() -> pd.DataFrame:
    cache_file = DOWNLOAD_DIR / _FILENAME
    if not exists(cache_file):
        response = requests.get(_CERVICAL_CANCER_URL, timeout=(10, 10))
        response.raise_for_status()
        zip_file = DOWNLOAD_DIR / 'temp.zip'
        with open(zip_file, 'wb') as z:
            z.write(response.content)

        with ZipFile(zip_file) as temp:
            temp.extract('risk_factors_cervical_cancer.csv', DOWNLOAD_DIR)

    with open(cache_file, 'rb') as file:
        return pd.read_csv(file)


if __name__ == '__main__':
    cancer = load_cervical_cancer()
    print(cancer.head())
