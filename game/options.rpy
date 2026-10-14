## Configuración general del juego (spec §7).

define config.name = _("Los orígenes: del ecosistema a la cultura")
define config.version = "2.0"
define config.window_title = "Los orígenes: del ecosistema a la cultura"
define config.save_directory = "LosOrigenes-educativo"
define build.name = "LosOrigenes"

define config.window = "hide"
define config.check_conflicting_properties = True
define config.default_music_volume = 0.35

## La voz lee cada bloque: el texto aparece completo de inmediato.
define config.default_text_cps = 0

init python:
    gui.init(1920, 1080)

    # Puntero de presentación y flechas: AvPág y → avanzan; RePág y ← retroceden.
    config.keymap["rollforward"].remove("anyrepeat_K_PAGEDOWN")
    config.keymap["dismiss"].extend(["K_PAGEDOWN", "K_RIGHT"])
    config.keymap["rollback"].append("K_LEFT")

    # Nada de la parte de desarrollo viaja en los paquetes del juego.
    for _patron in ("*.py", "*.toml", "*.lock", "*.md", "*.sh", "*.txt", ".python-version", "tests/**",
                    "docs/**", "references/**", "prompt.md", "game/tests/**", "game/audio/voz/manifest.json"):
        build.classify(_patron, None)
