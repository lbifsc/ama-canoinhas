# Configurando o projeto
## Clonar o repositório:
``
git clone https://github.com/Gustavo-F/ama-canoinhas.git
``

## Criar ambiente virtual:
``
python3 -m venv venv
``

## Ativar ambiente virtual:
``
source venv/bin/activate 
``

## Instalar dependências:
### Instalação e atualização do PIP:
``
python -m pip install --upgrade pip
``

### Baixar e instalar dependências:
``
pip install -r requirements.txt
``

## Crie o arquivo 'local_settings.py' dentro do diretório 'mysite'.
## Gere e copie uma SECRET_KEY neste site:
[https://djecrety.ir/](https://djecrety.ir/)

## No local_settings.py crie a variável 'SECRET_KEY' e atribua a ela a key gerada anteriormente:
``
SECRET_KEY = 'key_gerada' 
`` 
## Configuração do Banco de Dados MySQL:
### Adicione o código abaixo, com suas devidos valores, no local_settings.
### Lembre-se de criar o banco de dados no SGBD do MySQL.
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nome_banco',
        'HOST': 'host_mysql',
        'PORT': 'porta',
        'USER': 'usuario_mysql',
        'PASSWORD': 'senha',
    }
}
```

## Após isso basta fazer as migrações:
```
python manage.py makemigrations
python manage.py migrate
```
## Rodando o servidor de forma local:
### Observação: para iniciar o servidor é necessário ativar o ambiente virtual!
``
python manage.py runserver
``
### Caso a porta 8000 esteje ocupada é necessário informar outra porta a ser utilizada:
``
python manage.py runserver 127.0.0.1:porta_desejada
``