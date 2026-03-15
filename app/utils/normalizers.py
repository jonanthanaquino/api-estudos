import re
from datetime import datetime


def limpar_cnpj(cnpj: str) -> str:
    """
    Remove qualquer caractere que não seja número do CNPJ.
    """

    if not cnpj:
        return None

    return re.sub(r"\D", "", cnpj)


def normalizar_data(data_str: str) -> str:
    """
    Converte data do formato brasileiro (DD/MM/YYYY)
    para o formato ISO (YYYY-MM-DD) usado pelo PostgreSQL.
    """
    if not data_str:
        return None

    return datetime.strptime(data_str.strip(), "%d/%m/%Y").strftime("%Y-%m-%d")
