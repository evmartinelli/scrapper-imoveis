import logging
import httpx
from bs4 import BeautifulSoup
from typing import List
from itertools import repeat
from more_itertools import chunked
from concurrent.futures import ThreadPoolExecutor
from app.models.imovel import Imovel
from app.utils.parser import parse_imoveis_html, parse_detalhe_html

PESQUISA_URL = "https://venda-imoveis.caixa.gov.br/sistema/carregaPesquisaImoveis.asp"
LISTA_URL = "https://venda-imoveis.caixa.gov.br/sistema/carregaListaImoveis.asp"
DETALHE_URL = "https://venda-imoveis.caixa.gov.br/sistema/detalhe-imovel.asp"

HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://venda-imoveis.caixa.gov.br",
    "Referer": "https://venda-imoveis.caixa.gov.br/sistema/busca-imovel.asp?sltTipoBusca=imoveis"
}

logger = logging.getLogger(__name__)

def buscar_detalhes_imovel_sync(codigo: str, estado: str, cidade_id: str) -> dict:
    logger.info(f"Buscando detalhes do imóvel {codigo} - {estado} - {cidade_id}")
    
    with httpx.Client(follow_redirects=True) as client:
        response = client.post(DETALHE_URL, data={
            "hdnimovel": codigo,
            "hdn_estado": estado, 
            "hdn_cidade": cidade_id,
            "hdnorigem": "buscaimovel",
        }, headers=HEADERS)

        if response.status_code != 200:
            return {}

        return parse_detalhe_html(response.text)

async def buscar_imoveis(estado: str, cidade_id: str) -> List[Imovel]:
    async with httpx.AsyncClient() as client:
        dados_busca = {
            "hdn_estado": estado,
            "hdn_cidade": cidade_id,
            "hdn_tp_imovel": "Selecione",
            "hdn_faixa_vlr": "Selecione",
            "hdn_area_util": "Selecione",
            "hdn_quartos": "Selecione",
            "hdn_vg_garagem": "Selecione"
        }

        logger.info(f"Iniciando Busca {estado} - {cidade_id}")
        
        resposta = await client.post(PESQUISA_URL, data=dados_busca, headers=HEADERS)
        
        logger.info(f"Busca concluída {estado} - {cidade_id}")

        soup = BeautifulSoup(resposta.text, "html.parser")

        codigos = []
        for i in range(1, 10):
            campo = soup.find("input", {"id": f"hdnImov{i}"})
            if campo and campo.get("value"):
                codigos.extend(campo["value"].split("||"))

        if not codigos:
            return []

        todos_imoveis = []
        for grupo in chunked(codigos, 10):
            hdnImov = "||".join(grupo)
            resposta_detalhes = await client.post(
                LISTA_URL,
                data={"hdnImov": hdnImov},
                headers=HEADERS
            )
            imoveis = parse_imoveis_html(resposta_detalhes.text)
            todos_imoveis.extend(imoveis)

    # Fetch de detalhes em paralelo com threads
    with ThreadPoolExecutor(max_workers=10) as executor:
        detalhes_list = list(executor.map(
            buscar_detalhes_imovel_sync,
            [i.codigo for i in todos_imoveis],
            repeat(estado),
            repeat(cidade_id)
        ))

    for imovel, detalhes in zip(todos_imoveis, detalhes_list):
        for chave, valor in detalhes.items():
            setattr(imovel, chave, valor)

    return todos_imoveis
