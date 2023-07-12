from pydantic import BaseModel
from typing import Optional, List
from model.hospede import Hospede

from schemas import ComentarioSchema


class HospedeSchema(BaseModel):
    """ Define como um novo hóspede a ser inserido e como deve ser representado
    """
    nome: str = "Luiz Otávio"
    quartos: int = 1
    dias: int = 2
    valor: int = 250

    
class UpdateHospedeSchema(BaseModel):
    """ Define como valor, quartos e dias de hospedagem podem ser atualizados no banco de dados
    """
    nome: str = "Luiz Otávio"
    quartos: Optional[int] = 1
    dias: Optional[int] = 2
    valor: Optional[int] = 250


class HospedeBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Esta será
        feita apenas com base no nome do hóspede.
    """
    nome: str = ""


class ListagemHospedesSchema(BaseModel):
    """ Define como uma listagem de hóspedes será retornada.
    """
    hospedes:List[HospedeSchema]


def apresenta_hospedes(hospedes: List[Hospede]):
    """ Retorna uma representação do hóspede seguindo o schema definido em
        HospedeViewSchema.
    """
    result = []
    for cliente in hospedes:
        result.append({
            "nome": cliente.nome,
            "quartos": cliente.quartos,
            "dias": cliente.dias,
            "valor": cliente.valor
        })

    return {"hospedes": result}


class HospedeViewSchema(BaseModel):
    """ Define como um hóspede será retornado: hóspede + comentários.
    """
    id: int = 1
    nome: str = "Luiz Otávio"
    quartos: int = 1
    dias: int = 2
    valor: float = 250
    total_cometarios: int = 1
    comentarios:List[ComentarioSchema]


class HospedeDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição de remoção.
    """
    mesage: str
    nome: str

def apresenta_hospede(hospede: Hospede):
    """ Retorna uma representação do hóspede seguindo o schema definido em HospedeViewSchema.
    """
    return {
        "id": hospede.id,
        "nome": hospede.nome,
        "quartos": hospede.quartos,
        "dias:": hospede.dias,
        "valor": hospede.valor,
        "total_cometarios": len(hospede.comentarios),
        "comentarios": [{"texto": c.comentario_recepcao} for c in hospede.comentarios]
    }
