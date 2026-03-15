# from app.scrapers.sefaz_scraper import buscar_pagina
# from app.parsers.nfce_parser import extrair_dados


# def processar_nfce(url: str):
#     pagina = buscar_pagina(url)

#     nota, produtos = extrair_dados(pagina)

#     resultado = {"nota": nota, "produtos": produtos}

#     return resultado

from app.scrapers.sefaz_scraper import buscar_pagina
from app.parsers.nfce_parser import extrair_dados
from app.utils.normalizers import limpar_cnpj


from app.repository.nfce_repository import (
    buscar_estabelecimento_por_cnpj,
    salvar_estabelecimento,
    salvar_nota,
    salvar_itens,
    buscar_nota,
)


def processar_nfce(url: str):
    pagina = buscar_pagina(url)

    nota, produtos = extrair_dados(pagina)

    # ------------------------------------------------
    # 1️⃣ verificar estabelecimento
    # ------------------------------------------------

    # estabelecimento = buscar_estabelecimento_por_cnpj(nota["cnpj"])
    cnpj_limpo = limpar_cnpj(nota["cnpj"])
    estabelecimento = buscar_estabelecimento_por_cnpj(cnpj_limpo)

    if not estabelecimento:
        dados_estabelecimento = {
            # "cnpj": nota["cnpj"],
            "cnpj": cnpj_limpo,
            "nome": nota["estabelecimento"],
            "endereco": nota["endereco"],
        }

        estabelecimento = salvar_estabelecimento(dados_estabelecimento)

    estabelecimento_id = estabelecimento["id"]

    # ------------------------------------------------
    # 2️⃣ salvar nota
    # ------------------------------------------------

    dados_nota = {
        "numero": nota["numero_nota"],
        "serie": nota["serie_nota"],
        "data_emissao": nota["data_emissao"],
        "hora_emissao": nota["hora_emissao"],
        "forma_pagamento": nota["forma_pagamento"],
        "protocolo": nota["protocolo"],
        "estabelecimento_id": estabelecimento_id,
    }

    # nota_salva = salvar_nota(dados_nota)
    # nota_id = nota_salva["id"]

    nota_existente = buscar_nota(
        dados_nota["numero"], dados_nota["serie"], estabelecimento_id
    )

    if nota_existente:
        nota_id = nota_existente["id"]

    else:
        nota_salva = salvar_nota(dados_nota)

        nota_id = nota_salva["id"]

    # ------------------------------------------------
    # 3️⃣ salvar itens
    # ------------------------------------------------

    itens_para_salvar = []

    for produto in produtos:
        itens_para_salvar.append(
            {
                "nota_id": nota_id,
                "descricao": produto["nome"],
                "codigo": produto["codigo"],
                "quantidade": produto["quantidade"],
                "unidade": produto["unidade"],
                "valor_unitario": produto["valor_unitario"],
                "valor_total": produto["valor_total"],
            }
        )

    salvar_itens(itens_para_salvar)

    return {"nota": nota, "produtos": produtos}
