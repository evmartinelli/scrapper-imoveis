import httpx
from bs4 import BeautifulSoup
from typing import List
from app.models.imovel import Imovel
from app.utils.parser import parse_imoveis_html

PESQUISA_URL = "https://venda-imoveis.caixa.gov.br/sistema/carregaPesquisaImoveis.asp"
LISTA_URL = "https://venda-imoveis.caixa.gov.br/sistema/carregaListaImoveis.asp"

HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://venda-imoveis.caixa.gov.br",
    "Referer": "https://venda-imoveis.caixa.gov.br/sistema/busca-imovel.asp?sltTipoBusca=imoveis"
}

async def buscar_imoveis(estado: str, cidade_id: str) -> List[Imovel]:
    async with httpx.AsyncClient() as client:
        # 1. Buscar os hdnImovN via POST
        dados_busca = {
            "hdn_estado": estado,
            "hdn_cidade": cidade_id,
            "hdn_tp_imovel": "Selecione",
            "hdn_faixa_vlr": "Selecione",
            "hdn_area_util": "Selecione",
            "hdn_quartos": "Selecione",
            "hdn_vg_garagem": "Selecione"
        }

        resposta = await client.post(PESQUISA_URL, data=dados_busca, headers=HEADERS)
        soup = BeautifulSoup(resposta.text, "html.parser")

        # 2. Extrair todos os hdnImovN e concatenar os valores
        codigos = []
        for i in range(1, 10):
            campo = soup.find("input", {"id": f"hdnImov{i}"})
            if campo and campo.get("value"):
                codigos.append(campo["value"])

        if not codigos:
            return []

        hdnImov = "||".join("||".join(c.split("||")) for c in codigos)

        # 3. Fazer o POST com os códigos para obter os dados
        resposta_detalhes = await client.post(
            LISTA_URL,
            data={"hdnImov": hdnImov},
            headers=HEADERS
        )

        # 4. Parsear HTML da lista de imóveis
        imoveis = parse_imoveis_html(resposta_detalhes.text)

        return imoveis
