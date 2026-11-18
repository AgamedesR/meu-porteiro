"""Erros de regra de negócio.

São levantados pelos services, que não conhecem HTTP. A tradução para
códigos de resposta (404, 409...) é feita no main.py.
"""

class ErroDeDominio(Exception):
    """Base de todos os erros de rega de negócio"""

class NaoEncontrado(ErroDeDominio):
    """O recurso pedido não existe"""

class Conflito(ErroDeDominio):
    """A operação entra em conflito com algo que já existe."""