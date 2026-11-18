"""Testes das rotas de morador."""


def cadastrar(client, condominio_id, unidade_id, nome, telefone):
    """Atalho para cadastrar um morador nos testes."""
    return client.post(
        f"/condominios/{condominio_id}/moradores",
        json={"unidade_id": unidade_id, "nome": nome, "telefone": telefone},
    )


def test_cria_morador_e_guarda_so_os_digitos_do_telefone(
    client, condominio, unidade
):
    resposta = cadastrar(
        client, condominio["id"], unidade["id"], "Maria", "(83) 99999-0000"
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["telefone"] == "83999990000"
    assert corpo["ativo"] is True


def test_aceita_telefone_com_codigo_do_pais(client, condominio, unidade):
    resposta = cadastrar(
        client, condominio["id"], unidade["id"], "Ana", "+55 83 97777-0000"
    )

    assert resposta.status_code == 201
    assert resposta.json()["telefone"] == "5583977770000"


def test_rejeita_telefone_curto(client, condominio, unidade):
    resposta = cadastrar(client, condominio["id"], unidade["id"], "Carlos", "123")

    assert resposta.status_code == 422


def test_lista_moradores_em_ordem_alfabetica(client, condominio, unidade):
    for nome, tel in [("Pedro", "83966660000"), ("Ana", "83977770000")]:
        cadastrar(client, condominio["id"], unidade["id"], nome, tel)

    resposta = client.get(f"/condominios/{condominio['id']}/moradores")

    nomes = [m["nome"] for m in resposta.json()]
    assert nomes == ["Ana", "Pedro"]


def test_unidade_inexistente_devolve_404(client, condominio):
    resposta = cadastrar(client, condominio["id"], 999, "Carlos", "83955550000")

    assert resposta.status_code == 404


def test_nao_cadastra_morador_em_unidade_de_outro_condominio(
    client, condominio, unidade_do_outro
):
    resposta = cadastrar(
        client, condominio["id"], unidade_do_outro["id"], "Carlos", "83955550000"
    )

    assert resposta.status_code == 404


def test_condominio_nao_enxerga_moradores_de_outro(
    client, condominio, unidade, outro_condominio
):
    cadastrar(client, condominio["id"], unidade["id"], "Maria", "83999990000")

    resposta = client.get(f"/condominios/{outro_condominio['id']}/moradores")

    assert resposta.json() == []