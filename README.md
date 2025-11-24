# CHATBOT DE ATENDIMENTO SIMULADO


## Este projeto consiste em mostrar uma simulação de um atendimento com chatbot a medida que o usuário envia mensagens para receber o atendimento

# Tecnologias Utilizadas

- Python(Django, Django Rest)
- Javascript(React, Vite)
- PostgreSQL
- Docker, Docker-Compose
- Makefile

# Como testar o projeto localmente

- Inicialmente você precisa ter o python, git, linux(ubuntu, debian ou qualquer distro) e Docker, após verificar se tudo está instalado corretamente, 
pode clonar o repositório na sua máquina

- Após você clonar o repostório na sua máquina, entre no projeto e abra o terminal na pasta root do projeto, agora pode seguir as seguintes instruções:

## Passo 1
- Acesse a pasta **backend**, e crie o seu virtualenv com o seguinte comando: ```python3 -m venv venv``` ou ```python -m venv venv```, agora acesse o virtualenv: ```source venv/bin/activate```, após isso digite o seguinte comando para instalar as depêndencias: pip install -r requirements.txt, feito isso, pode seguir par ao passo 2

## Passo 2
- No arquivo .env.example, descomente as variáveis de ambientes relacionadas ao banco de dados e do django, a variável **SECRET_KEY**, vai estar vazia, para gerar uma chave e preencher essa variável, acesse essa pasta: cd ./backend
e digite o seguinte comando: ```python generate_hash_key.py``` ou ```python3 generate_hash_key.py```, após isso você verá no terminal uma chave gerada, copie ela e coloque a variável **SECRET_KEY**

## Passo 3
- Agora que você descomentou preencheu as variáveis de ambiente, vamos gerar o ambiente containerizado(se você está na pasta **./backend**, digite no terminal ```cd ..```), digite o seguinte comando: ```make build``` ou ```sudo make build```,
após a build do container, digite o seguinte comando para subir o container:
```make up``` ou ```sudo make up```, após isso, se a construção foi bem sucessida, você pode acessar essa rota no seu navegador e testar a aplicação

## Estruturação do Projeto(Back-End)

- O backend está estruturado da seguinte maneira:



## Estruturação do Projeto(Front-End)

- O frontend está estruturado da seguinte maneira:


## Decisões

-