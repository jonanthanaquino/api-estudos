import re


def limpar_cnpj(cnpj: str) -> str:
    """
    Remove qualquer caractere que não seja número do CNPJ.
    """

    if not cnpj:
        return None

    return re.sub(r"\D", "", cnpj)
