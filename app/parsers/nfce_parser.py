def extrair_estabelecimento(pagina):
    elemento = pagina.find("div", class_="txtTopo")

    if elemento:
        return elemento.text.strip()

    return None


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


def extrair_dados(pagina):
    nota = {
        "estabelecimento": extrair_estabelecimento(pagina),
        "cnpj": extrair_cnpj(pagina),
        "endereco": extrair_endereco(pagina),
    }

    produtos = extrair_produtos(pagina)

    return nota, produtos
