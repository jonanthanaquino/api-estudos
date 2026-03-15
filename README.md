
# Arquitetura do projeto

```

projeto-sefaz/
│
├── .env
├── .gitignore
├── .python-version
├── README.md
├── app
│   ├── __init__
│   ├── api
│   │   └── routes.py
│   ├── database
│   │   ├── connection.py
│   │   └── supabase_client.py
│   ├── main.py
│   ├── models
│   │   └── schemas.py
│   ├── parsers
│   │   └── nfce_parser.py
│   ├── repository
│   │   ├── nfce_repository.py
│   │   └── test_supabase.py
│   ├── scrapers
│   │   └── sefaz_scraper.py
│   ├── services
│   │   └── nfce_service.py
│   └── utils
│       └── normalizers.py
├── arvore.py
├── notas.txt
├── original.py
├── pyproject.toml
└── uv.lock


```


# Estrutura do banco

```
estabelecimentos
│
├─ id
├─ cnpj
├─ nome
└─ endereco

notas
│
├─ id
├─ numero
├─ serie
├─ data_emissao
├─ hora_emissao
├─ forma_pagamento
├─ protocolo
└─ estabelecimento_id

itens
│
├─ id
├─ nota_id
├─ descricao
├─ codigo
├─ quantidade
├─ unidade
├─ valor_unitario
└─ valor_total

```





## Rodar a api
uvicorn app.main:app --reload