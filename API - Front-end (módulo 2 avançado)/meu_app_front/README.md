
---
## Como executar

Faça o download do projeto e abrir o arquivo index.html no seu browser.

Insira os dados "nome", "quartos", "valor" e "dias" nos campos, observando que estes três últimos devem ser preenchidos somente com números.

## Como executar através do Docker

Certifique-se de ter o [Docker](https://docs.docker.com/engine/install/) instalado e em execução em sua máquina.

Navegue até o diretório que contém o Dockerfile no terminal e seus arquivos de aplicação e
Execute **como administrador** o seguinte comando para construir a imagem Docker:

```
$ docker build -t webserver .
```

Uma vez criada a imagem, para executar o container basta executar, **como administrador**, seguinte o comando:

```
$ docker run -d -p 8080:80 webserver
```

Uma vez executando, para acessar o front-end, basta abrir o [http://localhost:8080/#/](http://localhost:8080/#/) no navegador.

## APIs externas

```
Openweather API com os códigos únicos: 

const apiKey = `acd83b3b3e4f8eb29071ebfe535d7a10`; - chave para utilização da API

const apiUrl = `https://api.openweathermap.org/data/2.5/weather?&lang=pt_br&units=metric&q=`; – Url criada com definição de linguagem e medida de temperatura
```