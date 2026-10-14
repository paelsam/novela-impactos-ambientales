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
