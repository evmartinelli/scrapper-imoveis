from fastapi import FastAPI
from mangum import Mangum
from app.api.v1.endpoints import router as imoveis_router
import logging

if logging.getLogger().hasHandlers():
    logging.getLogger().setLevel(logging.INFO)
else:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI(title="Scraper Imóveis Caixa")

app.include_router(imoveis_router, prefix="/v1/imoveis", tags=["Imóveis"])

@app.get("/health", tags=["Infra"])
def health_check():
    return {"status": "ok"}

handler = Mangum(app)