# HR_Management

O HR Management é um sistema para gerenciar os processos relacionados à administração de recursos humanos de uma organização. Ele inclui funcionalidades como gerenciamento de funcionários, controle de ausências, avaliações de desempenho e administração de folhas de pagamento.

## Tecnologias Usadas
- **Backend**: Django
- **Frontend**: NUXT (Vite framework)
- **Base de Dados**: PostgreSQL e MongoDB
- **Autenticação**: Django Rest Framework + JWT

## Instalação
### Backend
Para configurar e executar o backend, siga o guia detalhado abaixo:

# Guia de Execução do Projeto de Gestão de Funcionários

Este guia detalha os passos necessários para configurar, executar e testar o projeto, incluindo uma descrição dos comandos utilizados.

## Passos para Configuração e Execução

### 1. Criar o Ambiente Virtual
Crie um ambiente virtual para isolar as dependências do projeto.
```bash
python -m venv env
```

### 2. Ativar o Ambiente Virtual
Ative o ambiente virtual para que as bibliotecas sejam instaladas corretamente.
- No Windows:
  ```bash
  .\env\Scripts\activate
  ```
- No Linux/macOS:
  ```bash
  source env/bin/activate
  ```

### 3. Instalar as Dependências
Instale todas as dependências listadas no arquivo `requirements.txt`.
```bash
pip install -r requirements.txt
```

### 4. Navegar até o Diretório do Backend
Acesse o diretório onde se encontram os ficheiros de gestão do backend.
```bash
cd .\backend\HrManagement\
```

### 5. Criar a Base de Dados
Utilize o comando `database` para criar a base de dados relacional. Este comando executa os scripts SQL necessários para a estrutura inicial da base de dados.
```bash
python manage.py database
```

### 6. Popular a Base de Dados (Seeders)
Use o comando `seed` para gerar dados fictícios nas tabelas da base de dados. O parâmetro `--quantity` define a quantidade de registros a serem criados.
```bash
python manage.py seed --quantity 20
```

### 7. Testar a Integridade da Base de Dados
O comando `test` executa uma série de testes automáticos para validar a integridade das funções SQL, triggers e vistas materializadas configuradas.
```bash
python manage.py test
```

### 8. Executar o Servidor do Projeto
Execute o servidor de desenvolvimento para iniciar a aplicação.
```bash
python manage.py runserver
```

### 9. Depurar (Exibir URLs Disponíveis)
O comando `show_urls` exibe uma lista de todas as URLs configuradas no projeto, o que facilita a navegação e depuração.
```bash
python manage.py show_urls
```

### 10. Excluir a Base de Dados
#### a. Excluir Dados (Seeders)
O comando `delete` remove os dados inseridos pelas operações de seeders, preparando a base de dados para uma nova população.
```bash
python manage.py delete
```

#### b. Excluir Objetos da Base de Dados
Utilize o comando `database` com a flag `--drop` para remover completamente os objetos (tabelas, funções, vistas) da base de dados.
> **Importante**: Certifique-se de excluir os dados (seeders) antes de excluir os objetos.
```bash
python manage.py database --drop
```

## Descrição dos Comandos

### Comando `database`
- **Função**: Cria e exclui a base de dados, além de executar scripts SQL.
- **Parâmetros**:
  - `--create`: Cria a base de dados.
  - `--drop`: Exclui a base de dados.
  - `--file <path>`: Executa um arquivo SQL especificado.

### Comando `seed`
- **Função**: Gera e insere dados de teste nas tabelas da base de dados.
- **Parâmetros**:
  - `--quantity <n>`: Define a quantidade de registros a serem inseridos (mínimo 10, máximo 10.000).
  - `--seeder <name>`: Executa um arquivo seeder específico.

### Comando `delete`
- **Função**: Exclui os dados inseridos pelas operações de seeders.
- **Parâmetros**:
  - `--seeder <name>`: Exclui dados com base em um seeder específico.

### Comando `test`
- **Função**: Executa testes automáticos de integridade da base de dados.

### Comando `show_urls`
- **Função**: Exibe todas as URLs configuradas no projeto.

---

### Frontend
Para configurar e executar o frontend, siga os passos abaixo:

### 1. Navegar até o Diretório do Frontend
```bash
cd nuxt
```

### 2. Instalar as Dependências
```bash
npm install
```

### 3. Executar o Servidor de Desenvolvimento
```bash
npm run dev
```


## Configuração do Arquivo `.env`
Tanto o backend quanto o frontend exigem a criação de um arquivo `.env` para armazenar as variáveis de ambiente necessárias ao funcionamento correto do sistema. Ambos contêm arquivos `env.example` como modelo.

### Backend
No backend, o arquivo `.env` deve conter as seguintes variáveis de ambiente:

- **DATABASE_NAME**: Nome da base de dados PostgreSQL.
- **DATABASE_USER**: Utilizador da base de dados.
- **DATABASE_PASSWORD**: Palavra-passe da base de dados.
- **DATABASE_HOST**: Endereço do servidor da base de dados.
- **DATABASE_PORT**: Porta do servidor da base de dados.
- **MONGO_HOST**: Endereço do servidor MongoDB.
- **MONGO_PORT**: Porta do servidor MongoDB.
- **MONGO_USER**: Utilizador do MongoDB.
- **MONGO_PASSWORD**: Palavra-passe do MongoDB.
- **MONGO_DATABASE_NAME**: Nome da base de dados MongoDB.
- **MONGO_AUTH_SOURCE**: Fonte de autenticação do MongoDB.
- **SECRET_KEY**: Chave secreta usada para a autenticação JWT.
- **DEBUG**: Define se o modo de depuração está ativado.

> **Nota**: Quando o modo `DEBUG` está ativado, algumas rotas não requerem autenticação, facilitando o desenvolvimento e os testes.


### Frontend
No frontend, o arquivo `.env` deve conter a seguinte variável de ambiente:

- **API_URL**: URL da API backend.


Este guia fornece uma descrição detalhada dos comandos e dos passos necessários para iniciar, popular, testar e depurar o projeto, garantindo uma experiência de desenvolvimento mais eficiente.


