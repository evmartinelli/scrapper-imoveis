import traceback
from bs4 import BeautifulSoup
from typing import List, Optional
from app.models.imovel import Imovel


def parse_detalhe_html(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    detalhes = {
        "titulo": soup.select_one("#dadosImovel h5").text.strip() if soup.select_one("#dadosImovel h5") else "",
        "valor_avaliacao": "",
        "valor_minimo_venda_1": "",
        "valor_minimo_venda_2": "",
        "descricao": "",
        "endereco": "",
        "data_leilao_1": "",
        "data_leilao_2": "",
    }

    # Bloco com os valores
    valores_block = soup.select_one(".content p")
    if valores_block:
        texto = valores_block.get_text("\n")
        for linha in texto.split("\n"):
            if "Valor de avaliação" in linha:
                detalhes["valor_avaliacao"] = linha.split(":")[-1].strip()
            elif "1º Leilão" in linha:
                detalhes["valor_minimo_venda_1"] = linha.split(":")[-1].strip()
            elif "2º Leilão" in linha:
                detalhes["valor_minimo_venda_2"] = linha.split(":")[-1].strip()
    
    # Data do leilão
    data_leilao_block = soup.select(".related-box span")
    if data_leilao_block:
        leiloes = [s.text.strip() for s in data_leilao_block if "Data do" in s.text]
        if len(leiloes) >= 2:
            detalhes["data_leilao_1"] = leiloes[0].replace("Data do 1º Leilão -", "").strip()
            detalhes["data_leilao_2"] = leiloes[1].replace("Data do 2º Leilão -", "").strip()

    # Dados Complementares
    dados_complementares_block = soup.select(".content")
    if dados_complementares_block:
        for item in dados_complementares_block:
            for linha in item.find_all("span"):
                if "Tipo de imóvel" in linha.text:
                    detalhes["tipo_imovel"] = linha.text.split(":")[-1].strip()
                elif "Número do imóvel" in linha.text:
                    detalhes["numero_imovel"] = linha.text.split(":")[-1].strip()
                elif "Matrícula" in linha.text:
                    detalhes["matricula"] = linha.text.split(":")[-1].strip()
                elif "Comarca" in linha.text:
                    detalhes["comarca"] = linha.text.split(":")[-1].strip()
                elif "Ofício" in linha.text:
                    detalhes["oficio"] = linha.text.split(":")[-1].strip()
                elif "Inscrição imobiliária" in linha.text:
                    detalhes["inscricao_imobiliaria"] = linha.text.split(":")[-1].strip()
                elif "Área privativa" in linha.text:
                    detalhes["area_privativa"] = linha.text.split(":")[-1].strip()
                elif "Área do terreno" in linha.text:
                    detalhes["area_terreno"] = linha.text.split(":")[-1].strip()

    # Descrição
    desc_tag = soup.find("strong", string="Descrição:")
    if desc_tag and desc_tag.parent:
        detalhes["descricao"] = desc_tag.parent.get_text(strip=True).replace("Descrição:", "").strip()

    # Endereço
    endereco_tag = soup.find("strong", string="Endereço:")
    if endereco_tag and endereco_tag.parent:
        detalhes["endereco"] = endereco_tag.parent.get_text(strip=True).replace("Endereço:", "").strip()

   # Despesas e formas de pagamento
    formas_pagamento, despesas = parse_pagamento_e_despesas(soup)
    if formas_pagamento:
        detalhes["formas_pagamento"] = formas_pagamento
    if despesas:
        detalhes["despesas"] = despesas

    return detalhes

def parse_imoveis_html(html: str) -> List[Imovel]:
    soup = BeautifulSoup(html, "html.parser")
    resultado = []

    blocos = soup.select("ul.control-group")

    for bloco in blocos:
        try:
            # Código do imóvel (vem no onclick do botão de detalhes)
            onclick = bloco.select_one("a[onclick*='detalhe_imovel']")
            codigo = ""
            if onclick:
                import re
                match = re.search(r"detalhe_imovel\((\d+)\)", onclick.get("onclick"))
                if match:
                    codigo = match.group(1)

            # Endereço completo e descrição
            detalhes = bloco.select(".form-row .control-item span font")
            endereco = ""
            for detalhe in detalhes:
                if detalhe and "<br/>" in str(detalhe):
                    endereco = str(detalhe).split("<br/>")
                    endereco = [BeautifulSoup(e, "html.parser").text.strip() for e in endereco]
                    endereco = next((e for e in endereco if "," in e or "RUA" in e or "AVENIDA" in e), "")

            # Cidade e estado
            local_info = bloco.select_one("strong font")
            cidade = estado = ""
            if local_info:
                cidade_estado_raw = local_info.text.strip().split("|")[0].strip()
                if " - " in cidade_estado_raw:
                    cidade, *bairro = cidade_estado_raw.split(" - ")
                    cidade = cidade.strip()
                    estado = "SP"  # fixado pois já vem do filtro; pode ser dinâmico depois

            # Valor
            valor_raw = bloco.select_one("strong font")
            valor = ""
            if valor_raw and "R$" in valor_raw.text:
                valor = valor_raw.text.split("R$")[-1].strip()
                valor = "R$ " + valor

            # Situação (extrair resumo descritivo)
            info_font = bloco.select(".form-row font")
            situacao = ""
            if len(info_font) > 1:
                situacao = info_font[0].text.strip()

            resultado.append(Imovel(
                codigo=codigo,
                endereco=endereco,
                cidade=cidade,
                estado=estado,
                valor=valor,
                situacao=situacao
            ))

        except Exception as e:
            print(f"[ERRO] Falha ao buscar detalhes do imóvel {codigo}: {e}")
            traceback.print_exc()
            continue  # Silencia erros e continua

    return resultado

def parse_pagamento_e_despesas(soup: BeautifulSoup) -> tuple[Optional[List[str]], Optional[List[str]]]:
    formas_pagamento = []
    despesas = []

    pagamento_ativo = False
    despesas_ativas = False

    p_tag = soup.find(lambda tag: tag.name == "p" and "FORMAS DE PAGAMENTO ACEITAS" in tag.text)
    if not p_tag:
        return None, None

    for element in p_tag.descendants:
        if element.name == "br":
            continue

        if element.name == "i" and "fa-info-circle" in element.get("class", []):
            texto = element.next_sibling
            if texto:
                texto = texto.strip(" ").strip()
                if pagamento_ativo:
                    formas_pagamento.append(texto)
                elif despesas_ativas:
                    despesas.append(texto)

        if element.string and "FORMAS DE PAGAMENTO ACEITAS" in element.string:
            pagamento_ativo = True
            despesas_ativas = False

        if element.string and "REGRAS PARA PAGAMENTO DAS DESPESAS" in element.string:
            pagamento_ativo = False
            despesas_ativas = True

    return formas_pagamento if formas_pagamento else None, despesas if despesas else None
