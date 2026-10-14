import pytest

from generar_voz import duraciones, firma, leer_guion, main, planificar, texto_para_voz


def escribir(raiz, nombre, contenido):
    ruta = raiz / nombre
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(contenido, encoding="utf-8")
    return ruta


def test_lee_lineas_con_id_y_argumentos(tmp_path):
    escribir(tmp_path, "capitulos/cap2.rpy", '''
label cap2:
    n "Hace unos 13.000 años terminó la glaciación." id cap2_06
    ficha "Desapareció al terminar la glaciación." (show_titulo="Alce gigante", show_pagina="p. 15") id cap2_obs_alce
        pregunta "¿Qué relación hay?" id cap2_quiz
    n "Esta línea no tiene id."
    $ x = 1
''')
    assert leer_guion(tmp_path) == {
        "cap2_06": "Hace unos 13.000 años terminó la glaciación.",
        "cap2_obs_alce": "Desapareció al terminar la glaciación.",
        "cap2_quiz": "¿Qué relación hay?",
    }


def test_ignora_las_pruebas_del_juego(tmp_path):
    escribir(tmp_path, "tests/escenas_prueba.rpy", 'n "Prueba." id prueba_01\n')
    assert leer_guion(tmp_path) == {}


def test_id_repetido_es_error(tmp_path):
    escribir(tmp_path, "a.rpy", 'n "Uno." id cap1_01\n')
    escribir(tmp_path, "b.rpy", 'n "Dos." id cap1_01\n')
    with pytest.raises(ValueError, match="id repetido «cap1_01»"):
        leer_guion(tmp_path)


def test_interpolacion_no_permitida(tmp_path):
    escribir(tmp_path, "a.rpy", 'n "Tienes [aciertos] aciertos." id final_01\n')
    with pytest.raises(ValueError, match="interpolar"):
        leer_guion(tmp_path)


def test_texto_para_voz():
    entrada = '{i}Hacia{/i} el 7000 a.C. vivían 3 hab./km² y hace 13.000 años \\"así\\"'
    assert texto_para_voz(entrada) == ('Hacia el 7000 antes de Cristo vivían 3 habitantes por kilómetro '
                                       'cuadrado y hace trece mil años "así"')


def test_planificar_genera_faltantes_y_cambiadas():
    lineas = {"a_01": "Uno.", "a_02": "Dos.", "a_03": "Tres."}
    manifiesto = {"a_01": firma("Uno."), "a_02": firma("Texto viejo.")}
    pendientes, huerfanas = planificar(lineas, manifiesto, existentes={"a_01", "a_02", "viejo_09"})
    assert pendientes == ["a_02", "a_03"] and huerfanas == ["viejo_09"]


def test_main_genera_y_luego_no_repite(tmp_path, capsys):
    guion, voces = tmp_path / "game", tmp_path / "game" / "audio" / "voz"
    escribir(guion, "cap.rpy", 'n "Hacia el 7000 a.C." id cap3_01\n')
    textos = []

    def falso(texto):
        textos.append(texto)
        return [0.0] * 10

    def guardar(ruta, audio):
        ruta.write_bytes(b"ogg")

    assert main([], sintetizador=falso, guardar=guardar, raiz=guion, voces=voces) == 0
    assert textos == ["Hacia el 7000 antes de Cristo"] and (voces / "cap3_01.ogg").exists()
    textos.clear()
    assert main([], sintetizador=falso, guardar=guardar, raiz=guion, voces=voces) == 0
    assert textos == [] and "al día" in capsys.readouterr().out


def test_revisar_no_genera(tmp_path):
    guion, voces = tmp_path / "game", tmp_path / "game" / "audio" / "voz"
    escribir(guion, "cap.rpy", 'n "Uno." id cap1_01\n')
    assert main(["--revisar"], sintetizador=lambda t: 1 / 0, raiz=guion, voces=voces) == 0
    assert not (voces / "cap1_01.ogg").exists()


def test_duraciones_suma_minutos_por_parte(tmp_path):
    for nombre in ("cap1_01", "cap1_02", "intro_01"):
        (tmp_path / f"{nombre}.ogg").write_bytes(b"x")
    assert duraciones(tmp_path, medir=lambda ruta: 30.0) == {"cap1": 1.0, "intro": 0.5}


def test_duraciones_sin_observaciones_y_una_rama(tmp_path):
    archivos = {
        "cap2_01.ogg": 60.0,
        "cap2_obs_mamut.ogg": 60.0,
        "cap2_dec.ogg": 30.0,
        "cap2_dec_a.ogg": 30.0,
        "cap2_dec_b.ogg": 90.0,
    }
    for nombre in archivos:
        (tmp_path / nombre).write_bytes(b"x")
    assert duraciones(tmp_path, medir=lambda ruta: archivos[ruta.name]) == {"cap2": 3.0}

