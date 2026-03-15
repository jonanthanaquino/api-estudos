from app.scrapers.sefaz_scraper import buscar_pagina
from app.parsers.nfce_parser import extrair_dados


def processar_nfce(url: str):
    pagina = buscar_pagina(url)

    nota, produtos = extrair_dados(pagina)

    resultado = {"nota": nota, "produtos": produtos}

    return resultado
