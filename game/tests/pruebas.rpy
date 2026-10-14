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
        click "Capítulos"
        assert screen "indice" timeout 5
        click "Del Homo sapiens al Neolítico"
        assert screen "portada" timeout 10
        assert eval (capitulo_actual == "cap2")
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
        assert eval (kicker() == "CAP. 2 · DEL HOMO SAPIENS AL NEOLÍTICO")
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
        assert screen "nota_campo" timeout 5
        advance
        assert screen "idea_clave" timeout 5
        run Start("prueba_resumen")
        assert screen "resumen" timeout 10
        assert eval (aciertos == 0 and len(respondidas) == 0)
        advance until screen "fin" timeout 30
        click "Volver al menú"
        assert screen "main_menu" timeout 10

    testcase cap2:
        run Start("cap2")
        assert screen "portada" timeout 10
        advance until screen "explorar" timeout 180
        click "Alce gigante"
        assert screen "ficha" timeout 5
        click "Volver al paisaje"
        click "Continuar"
        advance until screen "explorar" timeout 180
        click "Continuar"
        advance until screen "quiz" timeout 180
        click "Cuando la fauna se agota"
        assert eval (respondidas.get("cap2_quiz") is True) timeout 5
        advance until screen "decision" timeout 60
        click "Porque la fauna se agotaba"
        assert screen "segun" timeout 5
        advance until screen "nota_campo" timeout 60
        advance until screen "idea_clave" timeout 60
        advance until eval (capitulo_actual == "cap3") timeout 60

    testcase capturas_cap2:
        run Start("cap2")
        assert screen "portada" timeout 10
        pause 1.5
        $ renpy.screenshot(config.basedir + "/.cache/capturas/cap2_1_portada.png")
        advance
        pause 1.5
        $ renpy.screenshot(config.basedir + "/.cache/capturas/cap2_2_bloque_lateral.png")
        advance until screen "explorar" timeout 180
        pause 1.5
        $ renpy.screenshot(config.basedir + "/.cache/capturas/cap2_3_explorar.png")
        click "Alce gigante"
        pause 1.5
        $ renpy.screenshot(config.basedir + "/.cache/capturas/cap2_4_ficha.png")
        click "Volver al paisaje"
        click "Continuar"
        advance until screen "explorar" timeout 240
        click "Continuar"
        advance until screen "quiz" timeout 240
        pause 1.0
        $ renpy.screenshot(config.basedir + "/.cache/capturas/cap2_5_quiz.png")
        click "Las mejores armas"
        pause 1.0
        $ renpy.screenshot(config.basedir + "/.cache/capturas/cap2_6_retro.png")

    testcase intro:
        run Start("intro")
        assert screen "portada" timeout 10
        advance until screen "explorar" timeout 180
        click "La laguna"
        assert screen "ficha" timeout 5
        click "Volver al paisaje"
        click "Continuar"
        advance until screen "quiz" timeout 240
        click "Una historia contada solo desde la política"
        assert eval (respondidas.get("intro_quiz") is True) timeout 5
        advance until screen "decision" timeout 60
        click "Por la relación"
        advance until eval (capitulo_actual == "cap1") timeout 120

    testcase cap1:
        run Start("cap1")
        assert screen "portada" timeout 10
        advance until screen "explorar" timeout 240
        click "China: ciervos"
        assert screen "ficha" timeout 5
        click "Volver al paisaje"
        click "Continuar"
        advance until screen "quiz" timeout 60
        click "Porque se hacía con instrumentos"
        assert eval (respondidas.get("cap1_quiz") is True) timeout 5
        advance until screen "decision" timeout 60
        click "Seguir la manada"
        advance until eval (capitulo_actual == "cap2") timeout 120

    testcase cap3:
        run Start("cap3")
        assert screen "portada" timeout 10
        advance until screen "explorar" timeout 240
        click "Alfarero"
        assert screen "ficha" timeout 5
        click "Volver al paisaje"
        click "Continuar"
        advance until screen "explorar" timeout 180
        click "Continuar"
        advance until screen "explorar" timeout 180
        click "Continuar"
        advance until screen "quiz" timeout 60
        click "Porque nombran a las especies que sobran"
        assert eval (respondidas.get("cap3_quiz") is True) timeout 5
        advance until screen "decision" timeout 60
        click "Los jóvenes fundan"
        advance until eval (capitulo_actual == "final") timeout 120

    testcase final:
        run Start("final")
        assert screen "bloque" timeout 10
        advance until screen "resumen" timeout 60
        assert eval (len(respondidas) == 0)
        advance until screen "fin" timeout 120
        click "Volver al menú"
        assert screen "main_menu" timeout 10

    testcase completo:
        click "Comenzar"
        advance until screen "explorar" timeout 240
        click "Continuar"
        advance until screen "quiz" timeout 240
        click "Una historia contada solo desde la política"
        advance until screen "decision" timeout 60
        click "Por la relación"
        advance until eval (capitulo_actual == "cap1") timeout 120
        advance until screen "explorar" timeout 240
        click "Continuar"
        advance until screen "quiz" timeout 60
        click "Porque ya había cultivos"
        assert eval (respondidas.get("cap1_quiz") is False) timeout 5
        advance until screen "decision" timeout 60
        click "Cazar todos"
        advance until eval (capitulo_actual == "cap2") timeout 120
        advance until screen "explorar" timeout 240
        click "Continuar"
        advance until screen "explorar" timeout 240
        click "Continuar"
        advance until screen "quiz" timeout 120
        click "Cuando la fauna se agota"
        advance until screen "decision" timeout 60
        click "Para tener más tiempo libre"
        advance until eval (capitulo_actual == "cap3") timeout 120
        advance until screen "explorar" timeout 240
        click "Continuar"
        advance until screen "explorar" timeout 240
        click "Continuar"
        advance until screen "explorar" timeout 240
        click "Continuar"
        advance until screen "quiz" timeout 120
        click "Porque nombran a las especies que sobran"
        advance until screen "decision" timeout 60
        click "Vuelven a la caza"
        advance until eval (capitulo_actual == "final") timeout 120
        advance until screen "fin" timeout 240
        assert eval (aciertos == 3 and len(respondidas) == 4)
        click "Créditos"
        assert screen "creditos" timeout 5
