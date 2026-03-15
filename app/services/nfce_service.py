from app.scrapers.sefaz_scraper import buscar_pagina
from app.parsers.nfce_parser import extrair_dados
from app.parsers.nfce_parser import pagina_eh_nfce_valida
from app.utils.normalizers import limpar_cnpj
from app.utils.normalizers import normalizar_data
from app.utils.url_validators import url_eh_sefaz


import time
import random
from datetime import datetime
import traceback


from app.repository.nfce_repository import (
    buscar_estabelecimento_por_cnpj,
    salvar_estabelecimento,
    salvar_nota,
    salvar_itens,
    buscar_nota,
)


def processar_nfce(url: str):
    if not url_eh_sefaz(url):
        raise ValueError("URL informada não pertence à SEFAZ")

    pagina = buscar_pagina(url)

    if not pagina_eh_nfce_valida(pagina):
        return {
            "status": "pagina_invalida",
            "mensagem": "A página não corresponde a uma NFC-e válida ou a nota ainda não foi autorizada.",
        }

    nota, produtos = extrair_dados(pagina)

    # ------------------------------------------------
    # 1️⃣ verificar estabelecimento
    # ------------------------------------------------

    # estabelecimento = buscar_estabelecimento_por_cnpj(nota["cnpj"])
    cnpj_limpo = limpar_cnpj(nota["cnpj"])
    data_emissao = normalizar_data(nota["data_emissao"])
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
        "data_emissao": data_emissao,  # nota["data_emissao"],
        "hora_emissao": nota["hora_emissao"],
        "forma_pagamento": nota["forma_pagamento"],
        "protocolo": nota["protocolo"],
        "estabelecimento_id": estabelecimento_id,
    }

    # nota_salva = salvar_nota(dados_nota)
    # nota_id = nota_salva["id"]
    # print("--------------------")
    # print(nota["data_emissao"])
    # print("--------------------")

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


# if __name__ == "__main__":
#     # lista de URLs para teste em lote
#     urls = [
#         "https://www.sefaz.mt.gov.br/nfce/consultanfce?p=51260109477652019610651100000027241902953355|2|1|1|37780E9EEC7023546CB9EF4EB15B5E3EE4734C32",
#         "https://www.sefaz.mt.gov.br/nfce/consultanfce?p=51240123014826001004653060001954881214211623|2|1|1|ef586c39af7d495041c8861909b45ecc1439392c",
#         # você pode adicionar mais aqui
#     ]

#     for url in urls:
#         print("\n" + "=" * 60)
#         print("Processando:", url)

#         try:
#             resultado = processar_nfce(url)

#         #     print("Resultado:", resultado)

#         # except Exception as e:
#         #     print("Erro ao processar nota:", str(e))

#         except Exception as e:
#             print("Erro ao processar nota:")
#             traceback.print_exc()


# if __name__ == "__main__":
#     ARQUIVO_NOTAS = "notas-teste.txt"
#     ARQUIVO_LOG = "log_ingestao.txt"

#     DELAY_MIN = 2.5
#     DELAY_MAX = 4.5
#     DELAY_ERRO = 6

#     with open(ARQUIVO_NOTAS) as f:
#         urls = [linha.strip() for linha in f if linha.strip()]

#     total = len(urls)
#     sucesso = 0
#     erro = 0

#     print("\nIniciando ingestão de NFC-e")
#     print(f"Total de URLs: {total}")
#     print("-" * 60)

#     # cria arquivo de log
#     with open(ARQUIVO_LOG, "a", encoding="utf-8") as log:
#         log.write("\n" + "=" * 70 + "\n")
#         log.write(f"Execução iniciada em {datetime.now()}\n")
#         log.write("=" * 70 + "\n")

#         for i, url in enumerate(urls, start=1):
#             print(f"\n[{i}/{total}] Processando")

#             try:
#                 resultado = processar_nfce(url)

#                 status = "OK"

#                 sucesso += 1

#                 print("URL:", url)
#                 print("STATUS:", status)

#                 log.write(f"{datetime.now()} | OK | {url}\n")

#                 delay = random.uniform(DELAY_MIN, DELAY_MAX)

#                 print(f"Delay: {delay:.2f}s")

#                 time.sleep(delay)

#             except Exception as e:
#                 status = "ERRO"

#                 erro += 1

#                 print("URL:", url)
#                 print("STATUS:", status)
#                 print("MOTIVO:", str(e))

#                 log.write(f"{datetime.now()} | ERRO | {url} | {str(e)}\n")

#                 print(f"Delay erro: {DELAY_ERRO}s")

#                 time.sleep(DELAY_ERRO)

#         log.write("\nResumo:\n")
#         log.write(f"Total: {total}\n")
#         log.write(f"Sucesso: {sucesso}\n")
#         log.write(f"Erro: {erro}\n")
#         log.write("=" * 70 + "\n")

#     print("\n" + "=" * 60)
#     print("INGESTÃO FINALIZADA")
#     print(f"Total: {total}")
#     print(f"Sucesso: {sucesso}")
#     print(f"Erro: {erro}")
#     print("=" * 60)


import time
import random
import logging
from datetime import datetime


if __name__ == "__main__":
    ARQUIVO_NOTAS = "notas-teste.txt"

    DELAY_MIN = 2.5
    DELAY_MAX = 4.5
    DELAY_ERRO = 6

    # configuração do logger
    logging.basicConfig(
        filename="log_ingestao.txt",
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        encoding="utf-8",
    )

    # ler urls
    with open(ARQUIVO_NOTAS) as f:
        urls = [linha.strip() for linha in f if linha.strip()]

    total = len(urls)
    sucesso = 0
    erro = 0

    print("\nIniciando ingestão de NFC-e")
    print(f"Total de URLs: {total}")
    print("-" * 60)

    logging.info("=" * 70)
    logging.info("Execução iniciada")
    logging.info(f"Total de URLs: {total}")
    logging.info("=" * 70)

    for i, url in enumerate(urls, start=1):
        print(f"\n[{i}/{total}] Processando")
        print("URL:", url)

        try:
            resultado = processar_nfce(url)

            sucesso += 1

            logging.info(f"OK | {url}")

            delay = random.uniform(DELAY_MIN, DELAY_MAX)

            print("STATUS: OK")
            print(f"Delay: {delay:.2f}s")

            time.sleep(delay)

        except Exception as e:
            erro += 1

            logging.error(f"ERRO | {url} | {str(e)}")

            print("STATUS: ERRO")
            print("MOTIVO:", str(e))
            print(f"Delay erro: {DELAY_ERRO}s")

            time.sleep(DELAY_ERRO)

    logging.info("Resumo da execução")
    logging.info(f"Total: {total}")
    logging.info(f"Sucesso: {sucesso}")
    logging.info(f"Erro: {erro}")
    logging.info("=" * 70)

    print("\n" + "=" * 60)
    print("INGESTÃO FINALIZADA")
    print(f"Total: {total}")
    print(f"Sucesso: {sucesso}")
    print(f"Erro: {erro}")
    print("=" * 60)


# import logging
# import time
# import random
# from datetime import datetime

# import os

# os.makedirs("logs", exist_ok=True)


# if __name__ == "__main__":
#     ARQUIVO_NOTAS = "notas-teste.txt"

#     DELAY_MIN = 2.5
#     DELAY_MAX = 4.5
#     DELAY_ERRO = 6

#     # -----------------------------
#     # configuração do logger
#     # -----------------------------

#     logger = logging.getLogger("ingestao_nfce")
#     logger.setLevel(logging.INFO)

#     formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

#     # log de ingestão
#     handler_ingestao = logging.FileHandler("logs/ingestao.log", encoding="utf-8")
#     handler_ingestao.setLevel(logging.INFO)
#     handler_ingestao.setFormatter(formatter)

#     # log de erros
#     handler_erro = logging.FileHandler("logs/erros.log", encoding="utf-8")
#     handler_erro.setLevel(logging.ERROR)
#     handler_erro.setFormatter(formatter)

#     logger.addHandler(handler_ingestao)
#     logger.addHandler(handler_erro)

#     # -----------------------------
#     # leitura das urls
#     # -----------------------------

#     with open(ARQUIVO_NOTAS) as f:
#         urls = [linha.strip() for linha in f if linha.strip()]

#     total = len(urls)
#     sucesso = 0
#     erro = 0

#     print("\nIniciando ingestão de NFC-e")
#     print(f"Total de URLs: {total}")
#     print("-" * 60)

#     logger.info("=" * 60)
#     logger.info("Execução iniciada")
#     logger.info(f"Total de URLs: {total}")
#     logger.info("=" * 60)

#     for i, url in enumerate(urls, start=1):
#         print(f"\n[{i}/{total}] Processando")
#         print("URL:", url)

#         try:
#             resultado = processar_nfce(url)

#             sucesso += 1

#             logger.info(f"OK | {url}")

#             delay = random.uniform(DELAY_MIN, DELAY_MAX)

#             print("STATUS: OK")
#             print(f"Delay: {delay:.2f}s")

#             time.sleep(delay)

#         except Exception as e:
#             erro += 1

#             logger.error(f"ERRO | {url} | {str(e)}")

#             print("STATUS: ERRO")
#             print("MOTIVO:", str(e))
#             print(f"Delay erro: {DELAY_ERRO}s")

#             time.sleep(DELAY_ERRO)

#     logger.info("Resumo da execução")
#     logger.info(f"Total: {total}")
#     logger.info(f"Sucesso: {sucesso}")
#     logger.info(f"Erro: {erro}")
#     logger.info("=" * 60)

#     print("\n" + "=" * 60)
#     print("INGESTÃO FINALIZADA")
#     print(f"Total: {total}")
#     print(f"Sucesso: {sucesso}")
#     print(f"Erro: {erro}")
#     print("=" * 60)
