import requests
from bs4 import BeautifulSoup


def buscar_pagina(url: str) -> BeautifulSoup:
    """
    Faz requisição HTTP e retorna o HTML da página da NFC-e.
    """

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Erro ao acessar página da SEFAZ")

    pagina = BeautifulSoup(response.text, "html.parser")

    return pagina
