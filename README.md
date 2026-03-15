``

projeto-sefaz/
│
├── app/
│   │
│   ├── main.py              # inicializa FastAPI
│   │
│   ├── api/
│   │   └── routes.py        # endpoints da API
│   │
│   ├── services/
│   │   └── nfce_service.py  # lógica principal da aplicação
│   │
│   ├── scrapers/
│   │   └── sefaz_scraper.py # baixa HTML da página
│   │
│   ├── parsers/
│   │   └── nfce_parser.py   # extrai dados do HTML
│   │
│   ├── models/
│   │   └── schemas.py       # modelos de dados (Pydantic)
│   │
│   └── utils/
│       └── helpers.py       # funções auxiliares
│
├── tests/
│
├── pyproject.toml
│
└── README.md

``