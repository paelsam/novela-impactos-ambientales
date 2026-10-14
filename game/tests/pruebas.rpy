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
