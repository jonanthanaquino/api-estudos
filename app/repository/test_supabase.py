from app.repository.nfce_repository import salvar_estabelecimento


dados = {
    "cnpj": "12345678000100",
    "nome": "Supermercado Teste",
    "endereco": "Rua Teste",
}


resultado = salvar_estabelecimento(dados)

print(resultado)
