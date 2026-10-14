## Recorridos automáticos (./probar_juego.sh). No viajan en los paquetes del juego.

init python:
    _orig_main_menu_call = MainMenu.__call__
    def _safe_main_menu_call(self):
        if not renpy.context()._main_menu:
            _orig_main_menu_call(self)
    MainMenu.__call__ = _safe_main_menu_call
    MainMenu.get_sensitive = lambda self: True

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
        assert eval (capitulo_actual == "cap3") timeout 10

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



