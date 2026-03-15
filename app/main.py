from fastapi import FastAPI
from app.api.routes import router


app = FastAPI(
    title="NFCe Monitor",
    description="API para extração de cupons fiscais da SEFAZ",
)


app.include_router(router)
