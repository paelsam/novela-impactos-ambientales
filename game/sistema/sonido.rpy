## Música de fondo por momento y ambiente sonoro. El volumen de cada uno se ajusta en Opciones o en la pausa.

init python:
    # El ambiente (río, bosque, cueva) va por su propio canal, con el volumen de "Ambiente y efectos".
    renpy.music.register_channel("ambiente", mixer="sfx", loop=True)

define config.main_menu_music = "audio/musica/menu.ogg"
define config.default_music_volume = 0.35
define config.default_sfx_volume = 0.5

define CREDITOS_MUSICA = [
    "Menú: «Gymnopédie No. 1» (Erik Satie), interpretada por Kevin MacLeod (incompetech.com). CC BY 3.0.",
    "Momento 1: «Teller of the Tales», Kevin MacLeod (incompetech.com). CC BY 3.0.",
    "Momento 2: «Ancient Rite», Kevin MacLeod (incompetech.com). CC BY 4.0.",
    "Momento 3: «Hidden Past», Kevin MacLeod (incompetech.com). CC BY 3.0.",
    "Momentos 4 y 5: «La mañana», Peer Gynt (Edvard Grieg), Musopen Symphony Orchestra. Dominio público.",
    "Momento 6: «Dreams Become Real», Kevin MacLeod (incompetech.com). CC BY 3.0 (fragmento).",
]
