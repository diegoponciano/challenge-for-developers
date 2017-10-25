## Github Stars

Esse projeto se propõe a facilitar a organização de repositórios favoritos no Github, através de *tags*.

## Ambiente

Para facilitar o desenvolvimento, o projeto está estruturado em conteineres `docker`, com o `docker-compose`. Instale-os: [Docker](https://docs.docker.com/engine/installation/) e [Docker Compose](https://docs.docker.com/compose/install/#install-compose).  
Pra criar o ambiente e rodar o projeto, rode os seguintes comandos e abra o browser em http://localhost:8000:  
    
```bash
docker-compose build
docker-compose run --rm web python manage.py migrate
docker-compose up web
```

Para rodar comandos do Django no container, é só executá-los no container `web`, no seguinte formato:

```bash
docker-compose run --rm web <comando>
# exemplos:
docker-compose run --rm web python manage.py migrate  # aplica migrações do banco de dados
docker-compose run --rm web pytest  # executa os testes
```
## Sistema

Foi criado um *management command* pra baixar os repositórios de um usuário. O usuário deve existir na base (com o mesmo username do github).
```
python manage.py sync_repos <username>
```
Para adicionar ou remover tags, o usuário deve acessar o painel de administração do Django, e então acessar a lista de repositórios. Ao selecionar algum, haverá um campo `tags`.  
Na página inicial está disponível a busca dos repositórios, basta digitar uma tag (ou parte dela) e teclar `Enter`, ou clicar no botão de lupa, e o sistema buscará pelas tags cadastradas.