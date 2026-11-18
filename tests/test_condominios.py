"""Testes das rotas de condomínio."""


def test_cria_condominio_com_modo_de_aviso_padrao(client):
    resposta = client.post("/condominios", json={"nome": "Edifício Aurora"})

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["id"] == 1
    assert corpo["nome"] == "Edifício Aurora"
    assert corpo["modo_aviso"] == "todos"


def test_rejeita_nome_vazio(client):
    resposta = client.post("/condominios", json={"nome": ""})

    assert resposta.status_code == 422


def test_rejeita_modo_de_aviso_invalido(client):
    resposta = client.post(
        "/condominios", json={"nome": "Aurora", "modo_aviso": "qualquer"}
    )

    assert resposta.status_code == 422


def test_lista_condominios_em_ordem_alfabetica(client):
    client.post("/condominios", json={"nome": "Residencial Sol"})
    client.post("/condominios", json={"nome": "Edifício Aurora"})

    resposta = client.get("/condominios")

    assert resposta.status_code == 200
    nomes = [c["nome"] for c in resposta.json()]
    assert nomes == ["Edifício Aurora", "Residencial Sol"]