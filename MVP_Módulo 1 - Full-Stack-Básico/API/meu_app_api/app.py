from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import *
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
hospede_tag = Tag(name="Hospede", description="Adição, visualização e remoção de hóspedes na base de dados")
comentario_tag = Tag(name="Comentario", description="Adição de um comentário a um cliente cadastrado na base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/hospede', tags=[hospede_tag],
          responses={"200": HospedeViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_hospede(form: HospedeSchema):
    """Adiciona um novo hóspede à base de dados

    Retorna uma representação dos hóspedes e comentários associados.
    """
    hospede = Hospede(
        nome=form.nome,
        quartos=form.quartos,
        dias=form.dias,
        valor=form.valor
    )
    logger.debug(f"Adicionando hóspede de nome: '{hospede.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando hóspede
        session.add(hospede)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado hóspede de nome: '{hospede.nome}'")
        return apresenta_hospede(hospede), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Hóspede de mesmo nome já salvo na base de dados"
        logger.warning(f"Erro ao adicionar hóspede '{hospede.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo cliente :/"
        logger.warning(f"Erro ao adicionar hóspede '{hospede.nome}', {error_msg}")
        return {"mesage": error_msg}, 400
    
    
@app.post('/update_hospede', tags=[hospede_tag],
          responses={"200": HospedeViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def update_hospede(form: UpdateHospedeSchema):
    """Edita os dados de um hóspede já cadastrado na base de dados

    Retorna uma representação dos hóspedes e comentários associados.
    """
    nome_hospede = form.nome
    session = Session()
    
    try:
        db_hospede = session.query(Hospede).filter(Hospede.nome == nome_hospede).first()
        if not db_hospede:
            # se o cliente não foi encontrado
            error_msg = "Hóspede não encontrado na base :/"
            logger.warning(f"Erro ao buscar hóspede '{nome_hospede}', {error_msg}")
            return {"mesage": error_msg}, 404
    
        if form.quartos:
            db_hospede.quartos = form.quartos
            
                    
        if form.dias:
            db_hospede.dias = form.dias
        
        if form.valor:
            db_hospede.valor = form.valor

            
        session.add(db_hospede)
        session.commit()
        logger.debug(f"Dados do hóspede editados: '{db_hospede.nome}'")
        return apresenta_hospede(db_hospede), 200

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo cliente :/"
        logger.warning(f"Erro ao adicionar hóspede '{db_hospede.nome}', {error_msg}")
        return {"mesage": error_msg}, 400
    
    
@app.get('/hospedes', tags=[hospede_tag],
         responses={"200": HospedeViewSchema, "404": ErrorSchema})
def get_hospede(query: HospedeBuscaSchema):
    """Faz a busca por um hóspede a partir do nome do cliente

    Retorna uma representação dos hóspedes e comentários associados.
    """
    hospede_id = query.nome
    logger.debug(f"Coletando dados sobre cliente #{hospede_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    hospede = session.query(Hospede).filter(Hospede.nome == hospede_id).first()

    if not hospede:
        # se o cliente não foi encontrado
        error_msg = "Hóspede não encontrado na base :/"
        logger.warning(f"Erro ao buscar hóspede '{hospede_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Hóspede econtrado: '{hospede.nome}'")
        # retorna a representação de cliente
        return apresenta_hospede(hospede), 200


@app.get('/hospede', tags=[hospede_tag],
         responses={"200": ListagemHospedesSchema, "404": ErrorSchema})
def get_hospedes():
    """Faz a busca por todos os hóspedes cadastrados

    Retorna uma representação da listagem de clientes.
    """
    logger.debug(f"Coletando hóspedes")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    hospedes = session.query(Hospede).all()

    if not hospedes:
        # se não há hóspedes cadastrados
        return {"hospedes": []}, 200
    else:
        logger.debug(f"%d hóspedes econtrados" % len(hospedes))
        # retorna a representação de hóspedes
        print(hospedes)
        return apresenta_hospedes(hospedes), 200


@app.delete('/hospede', tags=[hospede_tag],
            responses={"200": HospedeDelSchema, "404": ErrorSchema})
def del_hospede(query: HospedeBuscaSchema):
    """Deleta um hóspede a partir do nome de cliente informado

    Retorna uma mensagem de confirmação da remoção.
    """
    hospede_nome = unquote(unquote(query.nome))
    print(hospede_nome)
    logger.debug(f"Deletando dados sobre cliente #{hospede_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Hospede).filter(Hospede.nome == hospede_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado cliente #{hospede_nome}")
        return {"mesage": "Hóspede removido", "id": hospede_nome}
    else:
        # se o cliente não foi encontrado
        error_msg = "Hóspede não encontrado na base de dados"
        logger.warning(f"Erro ao deletar cliente #'{hospede_nome}', {error_msg}")
        return {"mesage": error_msg}, 404

@app.post('/cometario', tags=[comentario_tag],
          responses={"200": HospedeViewSchema, "404": ErrorSchema})
def add_comentario(form: ComentarioSchema):
    """Adiciona de um novo comentário anexado ao cliente identificado pelo id

    Retorna uma representação dos clientes e comentários associados.
    """
    hospede_id  = form.hospede_id
    logger.debug(f"Adicionando comentários ao hóspede #{hospede_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo hóspede
    hospede = session.query(Hospede).filter(Hospede.id == hospede_id).first()

    if not hospede:
        # se cliente não encontrado
        error_msg = "Hóspede não encontrado na base de dados"
        logger.warning(f"Erro ao adicionar comentário ao hóspede '{hospede_id}', {error_msg}")
        return {"mesage": error_msg}, 404

    # criando o comentário
    comentario_recepcao = form.comentario_recepcao
    comentario = Comentario(comentario_recepcao)

    # adicionando o comentário ao cliente
    hospede.adiciona_comentario(comentario)
    session.commit()

    logger.debug(f"Adicionado comentário ao hóspede #{hospede_id}")

    # retorna a representação de cliente
    return apresenta_hospede(hospede), 200
