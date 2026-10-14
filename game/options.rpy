## Configuración general del juego.

define config.name = _("La fragilidad ambiental de la cultura")
define config.version = "1.6"
define config.window_title = "La fragilidad ambiental - Aventura educativa"
define config.save_directory = "FragilidadAmbiental-educativo"

define config.window = "auto"
define config.default_text_cps = 38

## Avisa de propiedades contradictorias en pantallas y transformaciones.
define config.check_conflicting_properties = True

init python:
    gui.init(960, 540)
