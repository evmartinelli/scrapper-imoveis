from bs4 import BeautifulSoup
from typing import List
from app.models.imovel import Imovel

def parse_imoveis_html(html: str) -> List[Imovel]:
    soup = BeautifulSoup(html, "html.parser")
    resultado = []

    # Exemplo baseado na estrutura visível da Caixa
    blocos = soup.select("div.resultadoBuscaImovel")

    for bloco in blocos:
        try:
            codigo = bloco.get("id", "")
            endereco = bloco.select_one(".enderecoImovel")
            cidade_estado = bloco.select_one(".cidadeEstado")
            valor = bloco.select_one(".valorImovel")
            situacao = bloco.select_one(".infoSituacao")

            resultado.append(Imovel(
                codigo=codigo.strip(),
                endereco=endereco.text.strip() if endereco else "",
                cidade=cidade_estado.text.split("/")[0].strip() if cidade_estado else "",
                estado=cidade_estado.text.split("/")[-1].strip() if cidade_estado else "",
                valor=valor.text.strip() if valor else "",
                situacao=situacao.text.strip() if situacao else ""
            ))
        except Exception as e:
            continue  # Silencia erros de parsing individual

    return resultado
