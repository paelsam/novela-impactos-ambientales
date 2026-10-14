"""Reglas del guion y de las pantallas que no cubre el lint de Ren'Py."""
import re
from pathlib import Path

import pytest

JUEGO = Path(__file__).parent.parent / "game"


def archivos_rpy():
    return [p for p in JUEGO.rglob("*.rpy") if "tests" not in p.relative_to(JUEGO).parts]


def test_ningun_texto_menor_de_18px():
    for archivo in archivos_rpy():
        for n, linea in enumerate(archivo.read_text(encoding="utf-8").splitlines(), start=1):
            for tamano in re.findall(r"(?:^|[\s_])size (\d+)\b", linea):
                assert int(tamano) >= 18, f"{archivo.name}:{n} usa size {tamano} (mínimo 18 px)"


def verificar_ideas_clave(texto_capitulos: str, capitulos_archivos: dict[str, str]) -> list[str]:
    """Compara las ideas del diccionario IDEAS con las líneas clave de los capítulos."""
    ideas = dict(re.findall(r'^\s*"(\w+)": "(.+)",$', texto_capitulos, re.M))
    errores = []
    for nombre, contenido in capitulos_archivos.items():
        for texto, parte in re.findall(r'^\s*clave "(.+)" id (\w+)_clave$', contenido, re.M):
            if ideas.get(parte) != texto:
                errores.append(f"La idea clave de {parte} en {nombre} no coincide con IDEAS")
    return errores


def test_verificar_ideas_clave_detecta_discrepancias():
    datos = 'IDEAS = {\n    "cap1": "Idea original.",\n}'
    capitulos = {"cap1.rpy": '    clave "Idea distinta." id cap1_clave'}
    errores = verificar_ideas_clave(datos, capitulos)
    assert len(errores) == 1
    assert "no coincide" in errores[0]


def test_ideas_clave_coinciden_con_los_capitulos():
    datos = (JUEGO / "sistema" / "capitulos.rpy").read_text(encoding="utf-8")
    capitulos = {p.name: p.read_text(encoding="utf-8") for p in (JUEGO / "capitulos").glob("*.rpy")}
    errores = verificar_ideas_clave(datos, capitulos)
    assert not errores, "\n".join(errores)


def verificar_quizzes(archivos_o_textos: dict[str, str]) -> list[str]:
    """Comprueba que cada menú de quiz tenga exactamente una opción con (correcta=True)."""
    errores = []
    for nombre, contenido in archivos_o_textos.items():
        lineas = contenido.splitlines()
        for n, linea in enumerate(lineas):
            if 'screen="quiz"' not in linea:
                continue
            sangria = len(linea) - len(linea.lstrip())
            bloque = []
            for siguiente in lineas[n + 1:]:
                if siguiente.strip() and len(siguiente) - len(siguiente.lstrip()) <= sangria:
                    break
                bloque.append(siguiente)
            correctas = sum("(correcta=True)" in b for b in bloque)
            if correctas != 1:
                errores.append(f"{nombre}:{n + 1}: el quiz tiene {correctas} opciones correctas (debe ser 1)")
    return errores


def test_verificar_quizzes_detecta_anomalias():
    texto_sin = """    menu (screen="quiz", quiz="q1", pagina="p. 1"):
        pregunta "¿Pregunta?" id q1
        "Opción A":
            pass
        "Opción B":
            pass"""
    texto_dos = """    menu (screen="quiz", quiz="q2", pagina="p. 2"):
        pregunta "¿Pregunta?" id q2
        "Opción A" (correcta=True):
            pass
        "Opción B" (correcta=True):
            pass"""
    errores = verificar_quizzes({"sin.rpy": texto_sin, "dos.rpy": texto_dos})
    assert len(errores) == 2
    assert "tiene 0 opciones correctas" in errores[0]
    assert "tiene 2 opciones correctas" in errores[1]


def test_cada_quiz_tiene_una_correcta():
    capitulos = {p.name: p.read_text(encoding="utf-8") for p in (JUEGO / "capitulos").glob("*.rpy")}
    errores = verificar_quizzes(capitulos)
    assert not errores, "\n".join(errores)
