import pytest

from ilustraciones import ErrorRegistro, cargar_registro

ENTRADA = '''
[[imagen]]
id = "cap2_glaciacion"
uso = "fondo"
tinta = "glaciacion"
url = "https://example.org/riou.jpg"
pagina_fuente = "https://example.org/riou"
autor = "Édouard Riou"
obra = "La Terre avant le déluge, lámina 10"
anio = 1863
licencia = "CC BY 4.0"
atribucion = "É. Riou (1863). Wellcome Collection, CC BY 4.0"
recorte = [63, 180, 2960, 1665]
'''


def escribir(tmp_path, texto):
    ruta = tmp_path / "fuentes.toml"
    ruta.write_text(texto, encoding="utf-8")
    return ruta


def test_carga_entrada_valida(tmp_path):
    [img] = cargar_registro(escribir(tmp_path, ENTRADA))
    assert img.id == "cap2_glaciacion"
    assert img.recorte == (63, 180, 2960, 1665)
    assert img.anio == "1863"
    assert (img.encaje, img.rotar, img.centrado) == ("cubrir", 0, (0.5, 0.5))


def test_acepta_recorte_automatico(tmp_path):
    texto = ENTRADA.replace("recorte = [63, 180, 2960, 1665]", 'recorte = "auto"')
    assert cargar_registro(escribir(tmp_path, texto))[0].recorte == "auto"


def test_rechaza_entrada_sin_licencia(tmp_path):
    texto = ENTRADA.replace('licencia = "CC BY 4.0"\n', "")
    with pytest.raises(ErrorRegistro, match="cap2_glaciacion: faltan licencia"):
        cargar_registro(escribir(tmp_path, texto))


def test_rechaza_tinta_inexistente(tmp_path):
    with pytest.raises(ErrorRegistro, match="tinta 'sepia' no existe"):
        cargar_registro(escribir(tmp_path, ENTRADA.replace('tinta = "glaciacion"', 'tinta = "sepia"')))


def test_rechaza_id_repetido(tmp_path):
    with pytest.raises(ErrorRegistro, match="id repetido"):
        cargar_registro(escribir(tmp_path, ENTRADA + ENTRADA))


def test_mapa_exige_limites(tmp_path):
    with pytest.raises(ErrorRegistro, match="mapa necesita"):
        cargar_registro(escribir(tmp_path, ENTRADA.replace('uso = "fondo"', 'uso = "mapa"')))


def test_reune_todos_los_errores(tmp_path):
    texto = (ENTRADA.replace('tinta = "glaciacion"', 'tinta = "sepia"')
             + ENTRADA.replace('id = "cap2_glaciacion"', 'id = "otra"').replace('autor = "Édouard Riou"\n', ""))
    with pytest.raises(ErrorRegistro) as error:
        cargar_registro(escribir(tmp_path, texto))
    assert "sepia" in str(error.value) and "otra: faltan autor" in str(error.value)
