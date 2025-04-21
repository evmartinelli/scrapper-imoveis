from fastapi import APIRouter, Query
from typing import List
from app.models.imovel import Imovel
from app.services.scraper import buscar_imoveis

router = APIRouter()

@router.get("/", response_model=List[Imovel])
async def listar_imoveis(
    estado: str = Query("SP", description="UF ex: SP"),
    cidade_id: str = Query("9205", description="Código da cidade ex: 9205 para Campinas")
):
    return await buscar_imoveis(estado=estado, cidade_id=cidade_id)
