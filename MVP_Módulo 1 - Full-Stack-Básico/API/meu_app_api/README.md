# Minha API

API para cadastro de novos hóspedes em um hotel, com informações sobre quartos alugados, valor total, dias de estadia; e com comentário opcional para a recepção do estabelecimento.

---
## Como executar 

Criar ambiente virtual com comando: 
```
python3 -m venv env
```
Em seguida, ativa a pasta do ambiente virtual com o comando: 
```
source env/bin/activate
```
O próximo passo será instalar as dependências/bibliotecas, descritas no arquivo, com o comando:
```
pip install -r requirements.txt
```
Por último, Para executar a API, basta executar:

```
flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento, utilizar o parâmetro reload, que reiniciará o servidor automaticamente após uma mudança no código fonte.

```
flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.
