from pydantic import BaseModel
from typing import List, Optional

class Imovel(BaseModel):
    codigo: Optional[str] = None
    titulo: Optional[str] = None
    endereco_resumido: Optional[str] = None
    tipo: Optional[str] = None
    descricao: Optional[str] = None
    detalhes_url: Optional[str] = None

    # Campos adicionados do detalhe
    valor_avaliacao: Optional[str] = None
    valor_minimo_venda_1: Optional[str] = None
    valor_minimo_venda_2: Optional[str] = None
    data_leilao_1: Optional[str] = None
    data_leilao_2: Optional[str] = None
    tipo_imovel: Optional[str] = None
    numero_imovel: Optional[str] = None
    matricula: Optional[str] = None
    comarca: Optional[str] = None
    oficio: Optional[str] = None
    inscricao_imobiliaria: Optional[str] = None
    area_privativa: Optional[str] = None
    area_terreno: Optional[str] = None
    edital: Optional[str] = None
    numero_item: Optional[str] = None
    leiloeiro: Optional[str] = None
    data_leilao_1: Optional[str] = None
    data_leilao_2: Optional[str] = None
    endereco: Optional[str] = None
    descricao_detalhada: Optional[str] = None
    formas_pagamento: Optional[List[str]] = None
    despesas: Optional[List[str]] = None
    observacoes: Optional[str] = None
