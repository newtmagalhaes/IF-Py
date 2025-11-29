import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent.absolute()
PASTA_ENEM_2024 = BASE_DIR / 'downloads/microdados_enem_2024/DADOS'
INPUT_FILE = PASTA_ENEM_2024 / 'RESULTADOS_2024.csv'
OUTPUT_FILE = PASTA_ENEM_2024 / 'RESULTADOS_2024_CE.csv'

iter_df = pd.read_csv(
    PASTA_ENEM_2024 / INPUT_FILE,
    sep=';',
    header=0,
    usecols=['SG_UF_PROVA'],
    encoding='windows-1252'
)

not_ce_rows = list(
    numero_linha
    for numero_linha, sigla in enumerate(iter_df['SG_UF_PROVA'], start=1)
    if sigla != 'CE'
)

print(f'{len(iter_df)} linhas, {len(iter_df) - len(not_ce_rows)} do Ceará')

df = pd.read_csv(
    INPUT_FILE,
    sep=';',
    header=0,
    index_col=0,
    encoding='windows-1252',
    skiprows=not_ce_rows,
)

df.to_csv(
    OUTPUT_FILE,
    chunksize=500,
)
print('csv escrito')
