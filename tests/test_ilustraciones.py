import urllib.error
import urllib.request

import pytest
import shapefile
from PIL import Image, ImageDraw

import ilustraciones
from ilustraciones import (
    TINTAS, UI, ErrorRegistro, Imagen, _hex, aplicar_tinta, cargar_registro, descargar, dibujar_mapa,
    encajar, generar_creditos, generar_ui, pieza, posicion_en_mapa, procesar, recorte_automatico,
    rejilla, rotar_y_recortar,
)

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


def entrada(**cambios):
    base = dict(id="x", uso="fondo", tinta="bosque", url="u", pagina_fuente="p", autor="a",
                obra="o", anio="1870", licencia="Dominio público", atribucion="a")
    base.update(cambios)
    return Imagen(**base)


def degradado(w=400, h=300):
    img = Image.new("L", (w, h))
    img.putdata([int(255 * (i % w) / (w - 1)) for i in range(w * h)])
    return img.convert("RGB")


def cerca(c1, c2, tol=24):
    return all(abs(a - b) <= tol for a, b in zip(c1, c2))


def test_tinta_lleva_negro_a_tinta_y_blanco_a_papel():
    img = aplicar_tinta(degradado(), "bosque")
    assert img.mode == "RGB" and img.size == (400, 300)
    assert cerca(img.getpixel((0, 150)), _hex(TINTAS["bosque"][0]))
    assert cerca(img.getpixel((399, 150)), _hex(TINTAS["bosque"][2]))


def test_tinta_es_determinista():
    assert aplicar_tinta(degradado(), "neolitico").tobytes() == aplicar_tinta(degradado(), "neolitico").tobytes()


def test_rotar_90_es_sentido_horario():
    img = Image.new("RGB", (40, 20), "white")
    img.putpixel((0, 0), (255, 0, 0))
    girada = rotar_y_recortar(img, entrada(rotar=90))
    assert girada.size == (20, 40)
    assert girada.getpixel((19, 0)) == (255, 0, 0)


def test_recorte_usa_x_y_ancho_alto():
    assert rotar_y_recortar(Image.new("RGB", (100, 80)), entrada(recorte=(10, 20, 30, 40))).size == (30, 40)


def test_recorte_fuera_de_la_imagen_falla():
    with pytest.raises(ValueError, match="x: el recorte .* se sale de la imagen"):
        rotar_y_recortar(Image.new("RGB", (100, 80)), entrada(recorte=(50, 0, 80, 40)))


def test_recorte_automatico_deja_fuera_margen_y_pie():
    pagina = Image.new("RGB", (1000, 1400), (240, 230, 210))
    d = ImageDraw.Draw(pagina)
    d.rectangle([100, 100, 900, 1100], fill=(40, 40, 40))       # el grabado
    d.rectangle([400, 1200, 600, 1215], fill=(40, 40, 40))      # el pie de imagen
    x, y, w, h = recorte_automatico(pagina)
    assert 100 <= x <= 110 and 100 <= y <= 110
    assert 1090 <= y + h <= 1100 and 890 <= x + w <= 900


def test_fondo_cubrir_llena_el_lienzo():
    assert encajar(degradado(1000, 1000), entrada()).size == (1920, 1080)


def test_fondo_editorial_deja_libre_el_panel_derecho():
    img = encajar(degradado(600, 900), entrada(encaje="editorial"))
    assert img.size == (1920, 1080)
    assert img.getpixel((1900, 540)) == _hex(TINTAS["bosque"][2])


def test_lamina_cabe_en_900():
    assert max(encajar(degradado(2000, 1000), entrada(uso="lamina")).size) == 900


def test_posicion_del_centro_es_el_centro():
    assert posicion_en_mapa(60, 47.5, (-15, 20, 135, 75)) == (0.5, 0.5)


def test_posiciones_de_los_marcadores_de_los_capitulos():
    eurasia = (-15, 20, 135, 75)
    assert posicion_en_mapa(110, 35, eurasia) == (0.811, 0.638)    # China
    assert posicion_en_mapa(-4, 40, eurasia) == (0.102, 0.583)     # España
    mundo = (-120, -40, 80, 60)
    assert posicion_en_mapa(-99, 19, mundo) == (0.131, 0.425)      # Mesoamérica


def test_mapa_pinta_tierra_y_deja_el_mar_en_papel(tmp_path):
    base = tmp_path / "tierra"
    with shapefile.Writer(str(base), shapeType=shapefile.POLYGON) as w:
        w.field("nombre", "C")
        w.poly([[(0, 0), (0, 10), (10, 10), (10, 0), (0, 0)]])
        w.record("cuadro")
    img = dibujar_mapa(base.with_suffix(".shp"), (-20, -20, 30, 30), "neolitico", tamano=(500, 500))
    papel = _hex(TINTAS["neolitico"][2])
    assert img.size == (500, 500)
    assert img.getpixel((5, 5)) == papel
    x, y = posicion_en_mapa(5, 5, (-20, -20, 30, 30), tamano=(500, 500))
    assert img.getpixel((round(x * 500), round(y * 500))) != papel


def test_pieza_tiene_esquinas_transparentes_y_centro_relleno():
    img = pieza((96, 96), 12, "#F3ECDCF5", "#CBBE9F", 2)
    assert img.mode == "RGBA" and img.size == (96, 96)
    assert img.getpixel((0, 0))[3] == 0
    assert all(abs(a - b) <= 1 for a, b in zip(img.getpixel((48, 48)), (0xF3, 0xEC, 0xDC, 0xF5)))


def test_generar_ui_escribe_todas_las_piezas(tmp_path):
    generar_ui(tmp_path)
    assert sorted(p.stem for p in tmp_path.glob("*.png")) == sorted([*UI, "filete"])


def test_descargar_usa_cache(tmp_path):
    origen = tmp_path / "x.jpg"
    Image.new("RGB", (10, 10)).save(origen)
    ruta = descargar(origen.as_uri(), tmp_path / "cache")
    assert ruta.read_bytes() == origen.read_bytes() and ruta.suffix == ".jpg"
    origen.unlink()
    assert descargar(origen.as_uri(), tmp_path / "cache") == ruta


def test_descargar_reintenta_ante_un_error(tmp_path, monkeypatch):
    origen = tmp_path / "x.png"
    Image.new("RGB", (4, 4)).save(origen)
    real = urllib.request.urlopen
    llamadas = []

    def falla_una_vez(peticion, timeout=None):
        llamadas.append(1)
        if len(llamadas) == 1:
            raise urllib.error.URLError("servidor caído")
        return real(peticion, timeout=timeout)

    monkeypatch.setattr(ilustraciones.urllib.request, "urlopen", falla_una_vez)
    ruta = descargar(origen.as_uri(), tmp_path / "cache", espera=0)
    assert ruta.read_bytes() == origen.read_bytes() and len(llamadas) == 2


def test_creditos_escapa_y_no_repite():
    a = entrada(atribucion="É. Riou [1863] {CC BY}", obra="Lámina 10", pagina_fuente="https://x")
    b = entrada(id="y", atribucion="É. Riou [1863] {CC BY}", obra="Lámina 10", pagina_fuente="https://x")
    texto = generar_creditos([a, b])
    assert texto.startswith("# Generado por ilustraciones.py")
    assert texto.count("Riou") == 1
    assert "[[1863]" in texto and "{{CC BY}" in texto


def test_rejilla_conserva_el_tamano():
    assert rejilla(degradado(200, 100)).size == (200, 100)


def test_procesar_rechaza_registro_invalido(tmp_path, capsys):
    ruta = tmp_path / "fuentes.toml"
    ruta.write_text('[[imagen]]\nid = "x"\n', encoding="utf-8")
    assert procesar(ruta) == 1
    assert "faltan" in capsys.readouterr().err

