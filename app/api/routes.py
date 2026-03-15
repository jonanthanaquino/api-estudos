from fastapi import APIRouter
from app.services.nfce_service import processar_nfce

router = APIRouter()


@router.post("/nfce")
def extrair_nfce(url: str):
    dados = processar_nfce(url)

    return dados
