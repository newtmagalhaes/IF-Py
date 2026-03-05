from datetime import datetime
import requests
import pandas as pd


def obter_cotacao_dolar(data_inicial, data_final):
    """pegando a contação do dolar no banco central.

    Retorna uma cotação diária.
    Consulta as cotações diárias do dólar no serviço PTAX do Banco Central.
    As datas devem estar no formato dd/mm/aaaa.
    """

    data_inicial_fmt = datetime.strptime(data_inicial, "%d/%m/%Y").strftime("%m-%d-%Y")
    data_final_fmt = datetime.strptime(data_final, "%d/%m/%Y").strftime("%m-%d-%Y")
    # Montagem da URL com as datas nos parâmetros
    url = (
        "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
        "CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)"
        f"?@dataInicial='{data_inicial_fmt}'&@dataFinalCotacao='{data_final_fmt}'"
        "&$top=10000&$format=json"
    )

    # Requisição HTTP GET
    resposta = requests.get(url)
    resposta.raise_for_status()  # dispara erro se o status não for 200

    # Conversão da resposta JSON
    dados = resposta.json().get("value", [])

    if not dados:
        raise Exception("Nenhum dado retornado para o período informado.")

    # Conversão em DataFrame ordenado pela data
    df = pd.DataFrame(dados)
    df["dataHoraCotacao"] = pd.to_datetime(df["dataHoraCotacao"])
    df = df.sort_values("dataHoraCotacao")

    # Renomeia colunas para facilitar a leitura
    df = df.rename(columns={
        "cotacaoCompra": "Compra",
        "cotacaoVenda": "Venda",
        "dataHoraCotacao": "DataHora"
    })

    return df[["DataHora", "Compra", "Venda"]]


def obter_cotacao(moeda = 'EUR',modo='diario', data_inicial='01/01/2024', data_final='01/01/2026'): # moedas : EUR, USD
    """Obter cotações de moedas do banco central.

    retorna varias cotações ao longo de um dia.
    Consulta as cotações do euro no serviço PTAX (OData) do Banco Central.
    Datas no formato dd/mm/aaaa.
    """
    data_inicial_fmt = datetime.strptime(data_inicial, "%d/%m/%Y").strftime("%m-%d-%Y")
    data_final_fmt = datetime.strptime(data_final, "%d/%m/%Y").strftime("%m-%d-%Y")

    url = (
        "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
        "CotacaoMoedaPeriodo(moeda=@moeda,dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)"
        f"?@moeda='{moeda}'&@dataInicial='{data_inicial_fmt}'&@dataFinalCotacao='{data_final_fmt}'"
        "&$top=10000&$format=json"
    )

    resposta = requests.get(url)
    resposta.raise_for_status()
    dados = resposta.json().get("value", [])

    if not dados:
        print("Nenhum dado retornado para o período informado.")
        return None

    df = pd.DataFrame(dados)
    df["dataHoraCotacao"] = pd.to_datetime(df["dataHoraCotacao"])
    df = df.sort_values("dataHoraCotacao")

    df = df.rename(columns={
        "cotacaoCompra": "Compra",
        "cotacaoVenda": "Venda",
        "dataHoraCotacao": "DataHora"
    })

    if modo == 'diario':
        df["Data"] = df["DataHora"].dt.date
        df = df.groupby("Data").last().reset_index()[["Data", "Compra", "Venda"]]

    return df


if __name__ == '__main__':
    from matplotlib import pyplot as plt
    from pprint import pprint

    data_inicial = "01/01/2024"
    data_final = "01/01/2026"
    df_cotacoes = obter_cotacao_dolar(data_inicial, data_final)

    pprint(df_cotacoes['Venda'].head(10))

    y = serieHistoricaDolar = df_cotacoes['Venda'].to_list()

    plt.figure(figsize=(18, 3))
    plt.style.use('dark_background')
    plt.plot(y, color='r')
    plt.xlabel('Períodos (dias)')
    plt.ylabel('Valor do Dólar em Reais')
    # plt.title('Variaçao do Dolar de Jun-2018 a Março 2019')
    plt.title('Variaçao do Dolar em 2024-2025')
    plt.grid(color='white', linestyle='--', linewidth=0.5)
    plt.show()
