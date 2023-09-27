from pydantic import BaseModel


class ComentarioSchema(BaseModel):
    """ Define como um novo comentário a ser inserido deve ser representado
    """
    hospede_id: int = 1
    comentario_recepcao: str = "Encaminhar ao cliente esclarecimentos sobre o fornecimento de café da manhã, WIFI e transporte para pontos turísticos."
