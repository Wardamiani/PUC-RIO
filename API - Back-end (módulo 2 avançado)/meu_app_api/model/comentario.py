from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union

from  model import Base


class Comentario(Base):
    __tablename__ = 'comentario'

    id_comentario = Column(Integer, primary_key=True)
    comentario_recepcao = Column(String(4000)) 
    # Definição do relacionamento entre o comentário/a dúvida que o hóspede tiver e o serviço.
    # Aqui está sendo definido a coluna 'hóspede' que vai guardar
    # a referencia ao serviço, a chave estrangeira que relaciona
    # um serviço ao comentário.    
    nome_hospede = Column(Integer, ForeignKey("hospede.Nome_hospede"), nullable=False)
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, comentario_recepcao:str, data_insercao:Union[DateTime, None] = None):
        """
        Cria um Comentário

        Arguments:
            comentario_recepcao: o texto de um comentário.
            data_insercao: data de quando o comentário foi feito ou inserido
                           à base
        """
        self.comentario_recepcao = comentario_recepcao
        if data_insercao:
            self.data_insercao = data_insercao
