from pydantic import BaseModel

class Imovel(BaseModel):
    codigo: str
    endereco: str
    cidade: str
    estado: str
    valor: str
    situacao: str
