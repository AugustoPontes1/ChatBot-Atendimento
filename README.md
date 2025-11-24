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
- Digite o seguinte comando para copiar as variáveis de ambiente para o arquivo **.env** com o seguinte comando: ```cp .env.example .env```, após isso,no arquivo **.env**, descomente as variáveis de ambientes relacionadas ao banco de dados e do django, a variável **SECRET_KEY**, vai estar vazia, para gerar uma chave e preencher essa variável, acesse essa pasta: cd ./backend
e digite o seguinte comando: ```python generate_hash_key.py``` ou ```python3 generate_hash_key.py```, após isso você verá no terminal uma chave gerada, copie ela e coloque a variável **SECRET_KEY**

## Passo 3
- Agora que você descomentou preencheu as variáveis de ambiente, vamos gerar o ambiente containerizado(se você está na pasta **./backend**, digite no terminal ```cd ..```), digite o seguinte comando: ```make build``` ou ```sudo make build```,
após a build do container, digite o seguinte comando para subir o container:
```make up``` ou ```sudo make up```, após isso, se a construção foi bem sucessida, você pode acessar essa rota no seu navegador e testar a aplicação:
http://localhost:5173/

# Estruturação do Projeto(Back-End)

- O backend está estruturado da seguinte maneira:

```
backend/
├── message/
│   ├── models.py          # Definição dos modelos de dados
│   ├── views.py           # Lógica da API (ViewSet)
│   ├── serializers.py     # Serialização dos dados
│   ├── urls.py            # Rotas da API
|   |__ utils.py           # Métodos para verificar o body da requisição
│   └── tests.py           # Testes unitários
├── configs/
│   └── settings.py        # Configurações do Django
└── manage.py
```

# Estruturação do Projeto(Front-End)

- O frontend está estruturado da seguinte maneira:
```
frontend/
├── src/
│   ├── App.jsx            # Componente principal
│   ├── App.css            # Estilos principais
│   └── main.jsx           # Ponto de entrada
├── package.json
└── vite.config.js
```

# Decisões

## Back-End
- Campos separados para usuário e bot: Permite distinguir claramente entre mensagens do usuário e respostas automatizadas

- USER_TYPE_CHOICES: Restringe os tipos de usuários possíveis, garantindo consistência nos dados

- Ordenação por data: Garante que as mensagens sejam exibidas em ordem cronológica

- Campos opcionais: null=True, blank=True permite flexibilidade para mensagens apenas do usuário ou apenas do bot

- Arquitetura da API
ViewSet com ações customizadas: Utilizamos Django REST Framework ViewSet com ```@action``` decorators para endpoints específicos **(login, logout, send_message, user_messages)**

- Sessões para autenticação: Optamos por sessões Django em vez de JWT para simplicidade em um projeto de escopo limitado

- Filtragem no servidor: A rota user_messages filtra mensagens no backend, garantindo que usuários só vejam suas próprias conversas

- Segurança e Validação
Verificação de sessão: Todas as ações verificam se o usuário está logado antes de processar

- Validação de entrada: Verificamos se o texto da mensagem não está vazio e se o usuário é válido

- Isolamento de dados: QuerySets filtrados por usuário logado previnem vazamento de informações entre usuários


## Front-End
- Estado local simples: Usei React hooks (useState, useEffect) em vez de Redux ou Context API devido à simplicidade da aplicação

- Persistência de sessão: Armazeno o usuário ativo no localStorage para manter o login entre recarregamentos de página

- Estado de loading e error: Feedback visual imediato para o usuário durante operações assíncronas

- Comunicação com API
Axios para requisições HTTP: Biblioteca robusta com interceptors e configurações globais

- Configuração de CORS: Configurado para trabalhar com credenciais e sessões

- Tratamento de erros: Feedback específico baseado nas respostas da API

- Interface do Usuário
Design responsivo: CSS flexbox para adaptação a diferentes tamanhos de tela

- Diferenciação visual: Cores distintas para mensagens do usuário, bot e outros estados

- Formulário controlado: Estado do input de mensagem gerenciado pelo React

## Devops
- Arquitetura Multi-container
Serviços separados: Backend, frontend e banco de dados em containers distintos

- Docker Compose: Orquestração simplificada dos serviços

- Makefile: Automação de comandos comuns para desenvolvimento

- Configurações de Desenvolvimento
Hot-reloading: Volumes montados permitem desenvolvimento com atualização em tempo real

- Variáveis de ambiente: Configuração flexível para diferentes ambientes

- Banco de dados persistente: Volume Docker para preservar dados entre reinicializações

## Testes
- Testes unitários abrangentes: Cobertura de login, logout, envio de mensagens e isolamento de dados

- Testes de integração: Verificação do fluxo completo entre usuários diferentes

- Testes de segurança: Garantia de que usuários não podem acessar dados de outros usuários

## Decisões de Design System
- Simplicidade sobre complexidade: Optei por soluções diretas em vez de arquiteturas superdimensionadas

- Experiência do usuário: Feedback imediato e interface intuitiva

- Segurança por padrão: Validações tanto no frontend quanto no backend

- Manutenibilidade: Código limpo, documentado e testado