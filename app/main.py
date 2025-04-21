from fastapi import FastAPI
from app.api.v1.endpoints import router as imoveis_router

app = FastAPI(title="Scraper Imóveis Caixa")

app.include_router(imoveis_router, prefix="/v1/imoveis", tags=["Imóveis"])
