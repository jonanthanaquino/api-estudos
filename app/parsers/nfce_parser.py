def extrair_estabelecimento(pagina):
    elemento = pagina.find("div", class_="txtTopo")

    if elemento:
        return elemento.text.strip()

    return None


def pagina_eh_nfce_valida(pagina):
    # texto = pagina.get_text()

    # marcador = "DOCUMENTO AUXILIAR DA NOTA FISCAL DE CONSUMIDOR ELETRÔNICA"
    texto = pagina.get_text().lower()
    marcador = "documento auxiliar da nota fiscal de consumidor eletrônica"

    if marcador in texto:
        return True

    return False


def extrair_cnpj(pagina):
    elemento = pagina.find_all("div", class_="text")[0]

    if elemento:
        texto = elemento.text.replace("\n", "").replace("\t", "")
        return texto[5:].strip()

    return None


def extrair_endereco(pagina):
    elemento = pagina.find_all("div", class_="text")[1]

    if elemento:
        texto = elemento.text.replace("\n", "").replace("\t", "")
        return texto.strip()

    return None


def extrair_produtos(pagina):
    lista_produtos = []

    produtos = pagina.find_all("table")[1].find_all("tr")

    for produto in produtos:
        nome = produto.find("span", class_="txtTit").get_text().strip()

        codigo = (
            produto.find("span", class_="RCod")
            .get_text()
            .replace("\n", "")
            .replace("\t", "")
        )[8:-1].strip()

        quantidade = (
            produto.find("span", class_="Rqtd").get_text()[6:].strip().replace(",", ".")
        )

        unidade = produto.find("span", class_="RUN").get_text()[3:].strip()

        valor_unitario = (
            (
                produto.find("span", class_="RvlUnit")
                .get_text()
                .replace("\n", "")
                .replace("\t", "")
            )[10:]
            .strip()
            .replace(",", ".")
        )

        valor_total = (
            produto.find("span", class_="valor").get_text().strip().replace(",", ".")
        )

        lista_produtos.append(
            {
                "nome": nome,
                "codigo": codigo,
                "quantidade": float(quantidade),
                "unidade": unidade,
                "valor_unitario": float(valor_unitario),
                "valor_total": float(valor_total),
            }
        )

    return lista_produtos


def extrair_forma_pagamento(pagina):
    elemento = pagina.find_all("label", class_="tx")[0]

    if elemento:
        return elemento.text.replace("\n", "").replace("\t", "").strip()

    return None


def extrair_numero_nota(pagina):
    elemento = pagina.find_all("ul")[0].find("li")

    texto = elemento.get_text(" ", strip=True).split()

    return texto[3] if len(texto) > 3 else None


def extrair_serie_nota(pagina):
    elemento = pagina.find_all("ul")[0].find("li")

    texto = elemento.get_text(" ", strip=True).split()

    return texto[5] if len(texto) > 5 else None


def extrair_data_emissao(pagina):
    elemento = pagina.find_all("ul")[0].find("li")

    texto = elemento.get_text(" ", strip=True).split()

    return texto[7] if len(texto) > 7 else None


def extrair_hora_emissao(pagina):
    elemento = pagina.find_all("ul")[0].find("li")

    texto = elemento.get_text(" ", strip=True).split()

    return texto[8] if len(texto) > 8 else None


def extrair_protocolo(pagina):
    elemento = pagina.find_all("ul")[0].find("li")

    texto = elemento.get_text(" ", strip=True).split()

    return texto[15] if len(texto) > 15 else None


def extrair_data_protocolo(pagina):
    elemento = pagina.find_all("ul")[0].find("li")

    texto = elemento.get_text(" ", strip=True).split()

    return texto[16] if len(texto) > 16 else None


def extrair_hora_protocolo(pagina):
    elemento = pagina.find_all("ul")[0].find("li")

    texto = elemento.get_text(" ", strip=True).split()

    return texto[17] if len(texto) > 17 else None


def extrair_dados(pagina):
    nota = {
        "estabelecimento": extrair_estabelecimento(pagina),
        "cnpj": extrair_cnpj(pagina),
        "endereco": extrair_endereco(pagina),
        "forma_pagamento": extrair_forma_pagamento(pagina),
        "numero_nota": extrair_numero_nota(pagina),
        "serie_nota": extrair_serie_nota(pagina),
        "data_emissao": extrair_data_emissao(pagina),
        "hora_emissao": extrair_hora_emissao(pagina),
        "protocolo": extrair_protocolo(pagina),
        "data_protocolo": extrair_data_protocolo(pagina),
        "hora_protocolo": extrair_hora_protocolo(pagina),
    }

    produtos = extrair_produtos(pagina)

    return nota, produtos
