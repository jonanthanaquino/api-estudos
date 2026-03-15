from app.database.supabase_client import supabase


# def salvar_estabelecimento(dados):
#     response = supabase.table("estabelecimentos").insert(dados).execute()

#     return response.data


# def salvar_nota(dados):
#     response = supabase.table("notas").insert(dados).execute()

#     return response.data


# def salvar_itens(lista_itens):
#     response = supabase.table("itens").insert(lista_itens).execute()

#     return response.data


def buscar_estabelecimento_por_cnpj(cnpj):
    response = supabase.table("estabelecimentos").select("*").eq("cnpj", cnpj).execute()

    if response.data:
        return response.data[0]

    return None


def buscar_nota(numero, serie, estabelecimento_id):
    response = (
        supabase.table("notas")
        .select("*")
        .eq("numero", numero)
        .eq("serie", serie)
        .eq("estabelecimento_id", estabelecimento_id)
        .execute()
    )

    if response.data:
        return response.data[0]

    return None


def salvar_estabelecimento(dados):
    response = supabase.table("estabelecimentos").insert(dados).execute()

    return response.data[0]


def salvar_nota(dados):
    response = supabase.table("notas").insert(dados).execute()

    return response.data[0]


def salvar_itens(lista_itens):
    response = supabase.table("itens").insert(lista_itens).execute()

    return response.data
