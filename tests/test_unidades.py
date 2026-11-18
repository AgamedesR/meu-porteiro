"""Testes das rotas de unidade."""


def test_cria_unidade(client, condominio):
    resposta = client.post(
        f"/condominios/{condominio['id']}/unidades",
        json={"andar": 9, "numero": "901"},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["condominio_id"] == condominio["id"]
    assert corpo["numero"] == "901"


def test_recusa_numero_repetido_no_mesmo_condominio(client, condominio, unidade):
    resposta = client.post(
        f"/condominios/{condominio['id']}/unidades",
        json={"andar": 9, "numero": "901"},
    )

    assert resposta.status_code == 409


def test_aceita_mesmo_numero_em_outro_condominio(
    client, unidade, unidade_do_outro
):
    # As duas fixtures já cadastraram a 901, cada uma no seu prédio
    assert unidade["numero"] == unidade_do_outro["numero"] == "901"
    assert unidade["condominio_id"] != unidade_do_outro["condominio_id"]


def test_condominio_inexistente_devolve_404(client):
    resposta = client.post(
        "/condominios/999/unidades", json={"andar": 9, "numero": "901"}
    )

    assert resposta.status_code == 404


def test_rejeita_andar_negativo(client, condominio):
    resposta = client.post(
        f"/condominios/{condominio['id']}/unidades",
        json={"andar": -1, "numero": "X"},
    )

    assert resposta.status_code == 422


def test_lista_so_as_unidades_do_proprio_condominio(
    client, condominio, unidade, unidade_do_outro
):
    client.post(
        f"/condominios/{condominio['id']}/unidades",
        json={"andar": 9, "numero": "902"},
    )

    resposta = client.get(f"/condominios/{condominio['id']}/unidades")

    numeros = [u["numero"] for u in resposta.json()]
    assert numeros == ["901", "902"]