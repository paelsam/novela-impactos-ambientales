## Recorridos automáticos (./probar_juego.sh). No viajan en los paquetes del juego.

init python:
    _orig_main_menu_call = MainMenu.__call__
    def _safe_main_menu_call(self):
        if not renpy.context()._main_menu:
            _orig_main_menu_call(self)
    MainMenu.__call__ = _safe_main_menu_call
    MainMenu.get_sensitive = lambda self: True

    _orig_start_call = Start.__call__
    def _safe_start_call(self):
        if renpy.exports.context_nesting_level() > 0:
            _orig_start_call(self)
        else:
            renpy.exports.jump(self.label)
    Start.__call__ = _safe_start_call

    _orig_test_run_end = renpy.test.testreporter.reporter.test_run_end
    def _test_run_end_and_quit():
        _orig_test_run_end()
        import sys
        sys.exit(1 if renpy.test.testreporter.reporter.has_failed else 0)
    renpy.test.testreporter.reporter.test_run_end = _test_run_end_and_quit

    _orig_advance_execute = renpy.test.testast.Advance.execute
    def _safe_advance_execute(self, state, t):
        if renpy.test.testast.Advance.began_newline or (t > 0 and renpy.exports.get_screen("explorar")):
            renpy.test.testast.next_node(self.next)
            return None
        return _orig_advance_execute(self, state, t)
    renpy.test.testast.Advance.execute = _safe_advance_execute



testsuite global:
    before testcase:
        run MainMenu(confirm=False)
        pause 1.0

    testcase navegacion:
        assert screen "main_menu" timeout 10
        click "Momentos"
        assert screen "momentos" timeout 5
        click "Cuando sobrevivir también transforma el entorno"
        assert screen "portada" timeout 10
        assert eval (capitulo_actual == "m3")
        advance
        assert screen "bloque" timeout 10

    testcase creditos:
        assert screen "main_menu" timeout 10
        click "Créditos"
        assert screen "creditos" timeout 5
        assert eval (any("Riou" in c[0] for c in CREDITOS_IMAGENES))
        click "Volver"
        assert screen "main_menu" timeout 5

    testcase narracion:
        run Start("prueba_narracion")
        assert screen "bloque" timeout 5
        assert eval (progreso("prueba_01") == ("prueba", 1, 3))
        assert eval (kicker() == "MOMENTO 3 · CUANDO SOBREVIVIR TAMBIÉN TRANSFORMA EL ENTORNO")
        assert eval (voz_de("no_existe") == "audio/voz/no_existe.ogg")
        advance
        assert eval (renpy.get_screen("bloque").scope["posicion"] == "lado") timeout 5
        keysym "K_PAGEDOWN"
        assert eval (renpy.get_screen("bloque").scope["posicion"] == "abajo") timeout 5
        keysym "K_LEFT"
        assert eval (renpy.get_screen("bloque").scope["posicion"] == "lado") timeout 5

    testcase observacion:
        run Start("prueba_observacion")
        assert screen "explorar" timeout 5
        click "Punto uno"
        assert screen "ficha" timeout 5
        assert eval ("uno" in vistos)
        click "Volver al paisaje"
        assert screen "explorar" timeout 5
        keysym "K_2"
        assert eval (punto_activo is not None and punto_activo.id == "dos") timeout 5
        advance
        assert screen "explorar" timeout 5
        click "Continuar"
        assert screen "bloque" timeout 5

    testcase quiz:
        run Start("prueba_quiz")
        assert screen "quiz" timeout 5
        click "Opción incorrecta"
        assert screen "retroalimentacion" timeout 5
        assert eval (aciertos == 0 and respondidas == {"prueba_quiz": False})
        assert eval (estado_quiz.correcta == 1 and estado_quiz.elegida == 0)
        assert eval (estado_quiz.pregunta == "¿Pregunta de prueba?")
        advance
        assert screen "quiz" timeout 5
        keysym "K_2"
        assert screen "retroalimentacion" timeout 5
        assert eval (aciertos == 0)
        advance
        assert screen "decision" timeout 5
        click "Camino B"
        assert screen "segun" timeout 5
        assert eval (estado_decision.elegida == 1)

    testcase pausa:
        run Start("prueba_narracion")
        assert screen "bloque" timeout 5
        keysym "K_ESCAPE"
        assert screen "pausa" timeout 5
        click "Reducir movimiento"
        assert eval (persistent.reducir_movimiento)
        click "Reducir movimiento"
        assert eval (not persistent.reducir_movimiento)
        click "Continuar"
        assert screen "bloque" timeout 5

    testcase cierre:
        run Start("prueba_cierre")
        assert screen "idea_clave" timeout 5
        run Start("prueba_fin")
        advance until screen "fin" timeout 30
        assert eval (aciertos == 0 and len(respondidas) == 0)
        click "Volver al menú"
        assert screen "main_menu" timeout 10

    testcase m1:
        run Start("momento1")
        assert screen "portada" timeout 10
        advance until screen "explorar" timeout 120
        click "La laguna"
        assert screen "ficha" timeout 5
        click "Volver al paisaje"
        click "Continuar"
        advance until screen "idea_clave" timeout 120
        advance until eval (capitulo_actual == "m2") timeout 60

    testcase m2:
        run Start("momento2")
        assert screen "portada" timeout 10
        advance until screen "quiz" timeout 180
        click "Los instrumentos, el fuego"
        assert eval (respondidas.get("m2_quiz") is True) timeout 5
        advance until eval (capitulo_actual == "m3") timeout 120

    testcase m3:
        run Start("momento3")
        assert screen "portada" timeout 10
        advance until screen "explorar" timeout 180
        click "Alce gigante"
        assert screen "ficha" timeout 5
        click "Volver al paisaje"
        click "Continuar"
        advance until screen "quiz" timeout 120
        click "Que la presión humana"
        assert eval (respondidas.get("m3_quiz") is True) timeout 5
        advance until eval (capitulo_actual == "m4") timeout 120

    testcase m4:
        run Start("momento4")
        assert screen "portada" timeout 10
        advance until screen "explorar" timeout 180
        click "Viviendas de madera"
        assert screen "ficha" timeout 5
        click "Volver al paisaje"
        click "Continuar"
        advance until screen "decision" timeout 120
        click "Los jóvenes fundan"
        assert screen "segun" timeout 5
        advance until eval (capitulo_actual == "m5") timeout 120

    testcase m5:
        run Start("momento5")
        assert screen "portada" timeout 10
        advance until screen "explorar" timeout 180
        click "Continuar"
        advance until screen "quiz" timeout 120
        click "Porque nombran a las especies"
        assert eval (respondidas.get("m5_quiz") is True) timeout 5
        advance until eval (capitulo_actual == "m6") timeout 120

    testcase m6:
        run Start("momento6")
        assert screen "portada" timeout 10
        advance until screen "fin" timeout 120
        click "Volver al menú"
        assert screen "main_menu" timeout 10

    testcase completo:
        click "Comenzar"
        advance until screen "explorar" timeout 180
        click "Continuar"
        advance until screen "quiz" timeout 300
        click "Los instrumentos, el fuego"
        advance until screen "explorar" timeout 180
        click "Continuar"
        advance until screen "quiz" timeout 120
        click "Que los cazadores cuidaban"
        assert eval (respondidas.get("m3_quiz") is False) timeout 5
        advance until screen "explorar" timeout 180
        click "Continuar"
        advance until screen "decision" timeout 120
        click "Vuelven a la caza"
        advance until screen "explorar" timeout 180
        click "Continuar"
        advance until screen "quiz" timeout 120
        click "Porque nombran a las especies"
        advance until screen "fin" timeout 180
        assert eval (aciertos == 2 and len(respondidas) == 3)
        click "Créditos"
        assert screen "creditos" timeout 5
