import pytest

from generar_voz import leer_guion, texto_para_voz


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
