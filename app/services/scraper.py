from typing import List
from app.models.imovel import Imovel

async def buscar_imoveis(estado: str, cidade_id: str) -> List[Imovel]:
    # Placeholder temporário até criarmos o scraper real
    return [
        Imovel(
            codigo="00000000000000",
            endereco="Rua Exemplo, 123",
            cidade="Campinas",
            estado="SP",
            valor="R$ 100.000,00",
            situacao="Desocupado"
        )
    ]
