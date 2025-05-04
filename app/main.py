from fastapi import FastAPI
from mangum import Mangum
from app.api.v1.endpoints import router as imoveis_router
import logging

if len(logging.getLogger().handlers) > 0:
    # The Lambda environment pre-configures a handler logging to stderr. If a handler is already configured,
    # `.basicConfig` does not execute. Thus we set the level directly.
    logging.getLogger().setLevel(logging.INFO)
else:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("Lambda inicializada - teste de log")

app = FastAPI(title="Scraper Imóveis Caixa")

app.include_router(imoveis_router, prefix="/v1/imoveis", tags=["Imóveis"])

@app.get("/health", tags=["Infra"])
def health_check():
    return {"status": "ok"}

handler = Mangum(app)