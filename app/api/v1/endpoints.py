from fastapi import APIRouter, Query
from app.services.scraper import buscar_imoveis
from app.models.imovel import Imovel
from typing import List

router = APIRouter()

@router.get("/", response_model=List[Imovel])
async def listar_imoveis(estado: str = "SP", cidade_id: str = "9205"):
    return await buscar_imoveis(estado=estado, cidade_id=cidade_id)
