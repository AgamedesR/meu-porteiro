# meu-porteiro

# Alembic: controlar mudanças na estrutura do banco sem apagar o arquivo toda vez. É o que permite evoluir o sistema com dados reais dentro.
#  alembic.ini        → configuração geral do Alembic
#  alembic/
#    env.py           → script que conecta o Alembic ao seu banco e aos seus modelos
#    versions/        → aqui ficam as migrações (um arquivo por mudança)
#    script.py.mako   → molde usado para gerar cada migração

# API: as primeiras rotas, começando por cadastrar condomínio e unidades e registrar uma encomenda (aqui entra a regra de gerar o código de retirada, na camada de serviço).