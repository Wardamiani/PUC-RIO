from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base, Comentario


class Hospede(Base):
    __tablename__ = 'hospede'

    id = Column("ID_cliente", Integer, primary_key=True)
    nome = Column("Nome_hospede", String(140), unique=True)
    quartos = Column(Integer)
    dias = Column(Integer)
    valor = Column(Float)
    data_insercao = Column(DateTime, default=datetime.now())

   # Definição do relacionamento entre o serviço e o comentário/dúvida do hóspede.
    # Essa relação é implicita, não está salva na tabela 'hospede',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    comentarios = relationship("Comentario")

    def __init__(self, nome:str, quartos:int, dias: int, valor:float, data_insercao:Union[DateTime, None] = None):
        """
        Cadastra um Hóspede

        Arguments:
            nome: nome do hóspede.
            quartos: quantos quartos o cliente alugará nos dias de permanencia no hotel
            valor: custo por cada quarto, de 125 por dia
            dias: quantos dias o hóspede terá de estadia
            data_insercao: data de quando o hóspede foi adicionado à base de dados
        """
        self.nome = nome
        self.quartos = quartos
        self.dias = dias
        self.valor = valor

        # se não for informada, será o data exata da inserção no banco de dados
        if data_insercao:
            self.data_insercao = data_insercao

    def adiciona_comentario(self, comentario:Comentario):
        """ Adiciona um novo comentário ou dúvida do cliente ao serviço
        """
        self.comentarios.append(comentario)

