"""Testes das rotas de usuário."""


def cadastrar(client, condominio_id, nome, papel):
    """Atalho para cadastrar um usuário nos testes."""
    return client.post(
        f"/condominios/{condominio_id}/usuarios",
        json={"nome": nome, "papel": papel},
    )


def test_cria_porteiro(client, condominio):
    resposta = cadastrar(client, condominio["id"], "Seu José", "porteiro")

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["papel"] == "porteiro"
    assert corpo["condominio_id"] == condominio["id"]
    assert corpo["ativo"] is True


def test_rejeita_papel_invalido(client, condominio):
    resposta = cadastrar(client, condominio["id"], "Fulano", "administrador")

    assert resposta.status_code == 422


def test_condominio_inexistente_devolve_404(client):
    resposta = cadastrar(client, 999, "Seu José", "porteiro")

    assert resposta.status_code == 404


def test_lista_usuarios_em_ordem_alfabetica(client, condominio):
    cadastrar(client, condominio["id"], "Sandra", "sindico")
    cadastrar(client, condominio["id"], "Antônio", "porteiro")

    resposta = client.get(f"/condominios/{condominio['id']}/usuarios")

    nomes = [u["nome"] for u in resposta.json()]
    assert nomes == ["Antônio", "Sandra"]


def test_condominio_nao_enxerga_usuarios_de_outro(
    client, condominio, outro_condominio
):
    cadastrar(client, condominio["id"], "Seu José", "porteiro")

    resposta = client.get(f"/condominios/{outro_condominio['id']}/usuarios")

    assert resposta.json() == []