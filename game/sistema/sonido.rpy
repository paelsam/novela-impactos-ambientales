## Música de fondo por momento y ambiente sonoro. El volumen de cada uno se ajusta en Opciones o en la pausa.

init python:
    # El ambiente (río, bosque, cueva) va por su propio canal, con el volumen de "Ambiente y efectos".
    renpy.music.register_channel("ambiente", mixer="sfx", loop=True)

define config.main_menu_music = "audio/musica/menu.ogg"

## Volúmenes iniciales, en la escala de los controles (0 a 1). Con un rango de 40 dB,
## la música al 35 % queda unos 26 dB por debajo de la voz: se oye de fondo sin taparla.
define config.volume_db_range = 40
define VOLUMEN_MUSICA = 0.35
define VOLUMEN_AMBIENTE = 0.5
define VOLUMEN_VOZ = 1.0
define config.default_music_volume = VOLUMEN_MUSICA
define config.default_sfx_volume = VOLUMEN_AMBIENTE
define config.default_voice_volume = VOLUMEN_VOZ

## Ren'Py solo aplica los valores iniciales la primera vez que se abre el juego. Este ajuste
## los aplica una vez más a quien ya lo había abierto (en el escritorio o en el navegador).
init 999 python:
    if persistent.volumenes_iniciales != 1:
        persistent.volumenes_iniciales = 1
        _preferences.set_mixer("music", VOLUMEN_MUSICA)
        _preferences.set_mixer("sfx", VOLUMEN_AMBIENTE)
        _preferences.set_mixer("voice", VOLUMEN_VOZ)

define CREDITOS_MUSICA = [
    "Menú: «Gymnopédie No. 1» (Erik Satie), interpretada por Kevin MacLeod (incompetech.com). CC BY 3.0.",
    "Momento 1: «Teller of the Tales», Kevin MacLeod (incompetech.com). CC BY 3.0.",
    "Momento 2: «Ancient Rite», Kevin MacLeod (incompetech.com). CC BY 4.0.",
    "Momento 3: «Hidden Past», Kevin MacLeod (incompetech.com). CC BY 3.0.",
    "Momentos 4 y 5: «La mañana», Peer Gynt (Edvard Grieg), Musopen Symphony Orchestra. Dominio público.",
    "Momento 6: «Dreams Become Real», Kevin MacLeod (incompetech.com). CC BY 3.0 (fragmento).",
]
