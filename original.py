import requests
from bs4 import BeautifulSoup
import pandas as pd


def buscar_pagina(url):
    response = requests.get(url)
    if response.status_code == 200:
        pagina = BeautifulSoup(response.text, "html.parser")
        print("Requisição OK!")
        return pagina
    else:
        print("URL inválida!")
        return None


def pegar_estabelecimento(pagina):
    if pagina is not None:
        elemento = pagina.find("div", class_="txtTopo")
        if elemento:
            return elemento.text
        else:
            print("Elemento inexistente")
            return None

    else:
        print("Página vazia!")

        return None


def pegar_cnpj(pagina):
    if pagina is not None:
        elemento = pagina.find_all("div", class_="text")[0]
        if elemento:
            return elemento.text.replace("\t", "").replace("\n", "")[5:].strip()
        else:
            print("Elemento inexistente")
            return None

    else:
        print("Página vazia!")

        return None


def pegar_endereco(pagina):
    if pagina is not None:
        elemento = pagina.find_all("div", class_="text")[1]
        if elemento:
            return elemento.text.replace("\t", "").replace("\n", "").strip()
        else:
            print("Elemento inexistente")
            return None

    else:
        print("Página vazia!")

        return None


def pegar_forma_pagamento(pagina):
    if pagina is not None:
        elemento = pagina.find_all("label", class_="tx")[0]
        if elemento:
            return elemento.text.replace("\t", "").replace("\n", "").strip()
        else:
            print("Elemento inexistente")
            return None

    else:
        print("Página vazia!")

        return None


def pegar_num_nota(pagina):
    if pagina is not None:
        elemento = pagina.find_all("ul")[0].find("li")
        elemento = elemento.get_text(" ", strip=True)
        elemento = elemento.split()
        elemento = elemento[3].strip()

        if elemento:
            return elemento
        else:
            print("Elemento inexistente")
            return None

    else:
        print("Página vazia!")

        return None


def pegar_serie_nota(pagina):
    if pagina is not None:
        elemento = pagina.find_all("ul")[0].find("li")
        elemento = elemento.get_text(" ", strip=True)
        elemento = elemento.split()
        elemento = elemento[5].strip()

        if elemento:
            return elemento
        else:
            print("Elemento inexistente")
            return None

    else:
        print("Página vazia!")

        return None


def pegar_data_emissao(pagina):
    if pagina is not None:
        elemento = pagina.find_all("ul")[0].find("li")
        elemento = elemento.get_text(" ", strip=True)
        elemento = elemento.split()
        elemento = elemento[7].strip()

        if elemento:
            return elemento
        else:
            print("Elemento inexistente")
            return None

    else:
        print("Página vazia!")

        return None


def pegar_hora_emissao(pagina):
    if pagina is not None:
        elemento = pagina.find_all("ul")[0].find("li")
        elemento = elemento.get_text(" ", strip=True)
        elemento = elemento.split()
        elemento = elemento[8].strip()

        if elemento:
            return elemento
        else:
            print("Elemento inexistente")
            return None

    else:
        print("Página vazia!")

        return None


def pegar_protocolo(pagina):
    if pagina is not None:
        elemento = pagina.find_all("ul")[0].find("li")
        elemento = elemento.get_text(" ", strip=True)
        elemento = elemento.split()
        elemento = elemento[15].strip()

        if elemento:
            return elemento
        else:
            print("Elemento inexistente")
            return None

    else:
        print("Página vazia!")

        return None


def pegar_data_protocolo(pagina):
    if pagina is not None:
        elemento = pagina.find_all("ul")[0].find("li")
        elemento = elemento.get_text(" ", strip=True)
        elemento = elemento.split()
        elemento = elemento[16].strip()

        if elemento:
            return elemento
        else:
            print("Elemento inexistente")
            return None

    else:
        print("Página vazia!")

        return None


def pegar_hora_protocolo(pagina):
    if pagina is not None:
        elemento = pagina.find_all("ul")[0].find("li")
        elemento = elemento.get_text(" ", strip=True)
        elemento = elemento.split()
        elemento = elemento[17].strip()

        if elemento:
            return elemento
        else:
            print("Elemento inexistente")
            return None

    else:
        print("Página vazia!")

        return None


def pegar_produtos(pagina):
    lista = []
    if pagina is not None:
        produtos = pagina.find_all("table")[1].find_all("tr")
        for produto in produtos:
            nome_produto = produto.find("span", class_="txtTit").get_text().strip()

            cod_produto = (
                produto.find("span", class_="RCod")
                .get_text()
                .replace("\t", "")
                .replace("\n", "")
            )[8:-1].strip()

            qtd_produto = (
                produto.find("span", class_="Rqtd")
                .get_text()[6:]
                .strip()
                .replace(",", ".")
            )

            uni_produto = produto.find("span", class_="RUN").get_text()[3:].strip()

            val_unit_produto = (
                (
                    produto.find("span", class_="RvlUnit")
                    .get_text()
                    .replace("\t", "")
                    .replace("\n", "")
                )[10:]
                .strip()
                .replace(",", ".")
            )

            val_total_produto = (
                produto.find("span", class_="valor")
                .get_text()
                .strip()
                .replace(",", ".")
            )

            dados = {
                "nome": nome_produto,
                "codigo": cod_produto,
                "quantidade": float(qtd_produto),
                "unidade": uni_produto,
                "valor_unitario": float(val_unit_produto),
                "valor_total": float(val_total_produto),
            }
            lista.append(dados)

        return pd.DataFrame(lista)


def extrair_dados_nota(pagina):
    dados_nota = {
        "estabelecimento": pegar_estabelecimento(pagina),
        "cnpj": pegar_cnpj(pagina),
        "endereco": pegar_endereco(pagina),
        "pagamento": pegar_forma_pagamento(pagina),
        "numero_nota": pegar_num_nota(pagina),
        "serie_nota": pegar_serie_nota(pagina),
        "data_emissao": pegar_data_emissao(pagina),
        "hora_emissao": pegar_hora_emissao(pagina),
        "protocolo": pegar_protocolo(pagina),
        "data_protocolo": pegar_data_protocolo(pagina),
        "hora_protocolo": pegar_hora_protocolo(pagina),
    }
    return pd.DataFrame([dados_nota])


def executar(url):
    pagina = buscar_pagina(url)
    dados_nota = extrair_dados_nota(pagina)
    produtos = pegar_produtos(pagina)
    numero = dados_nota["numero_nota"].iloc[0]
    produtos["numero_nota"] = numero
    print(dados_nota.head())
    print(produtos.head())
    return dados_nota, produtos


if __name__ == "__main__":
    # URL = input("Inserir a url aqui: ")
    URL = "https://www.sefaz.mt.gov.br/nfce/consultanfce?p=51260109477652019610651100000027241902953355|2|1|1|37780E9EEC7023546CB9EF4EB15B5E3EE4734C32"
    executar(URL)
