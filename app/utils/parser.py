from bs4 import BeautifulSoup
from typing import List
from app.models.imovel import Imovel

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
            detalhe = bloco.select_one(".form-row .control-item span font")
            endereco = ""
            if detalhe and "<br />" in str(detalhe):
                endereco = str(detalhe).split("<br />")
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

        except Exception:
            continue  # Silencia erros e continua

    return resultado
