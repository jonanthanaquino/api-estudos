from pydantic import BaseModel
from typing import List


class Produto(BaseModel):
    nome: str
    codigo: str
    quantidade: float
    unidade: str
    valor_unitario: float
    valor_total: float


class Nota(BaseModel):
    estabelecimento: str
    cnpj: str
    endereco: str


class NFCeResponse(BaseModel):
    nota: Nota
    produtos: List[Produto]
