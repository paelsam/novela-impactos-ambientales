"""Genera las narraciones del juego con Kokoro TTS (voz em_alex, español).

Uso: uv run generar_voz.py

Los WAV se guardan en game/audio/voice/. Los que ya existen se conservan:
borra un archivo para regenerarlo. La primera ejecución descarga el modelo.
"""

from pathlib import Path

import numpy as np
import soundfile as sf

VOICE_DIR = Path(__file__).parent / "game" / "audio" / "voice"
VOICE = "em_alex"
SPEED = 0.92
SAMPLE_RATE = 24000

# Deben coincidir con las tarjetas `mini_story` de game/script.rpy.
NARRATIONS = {
    "intro_01.wav": "Primera pista: la historia no ocurre en un escenario vacío.",
    "intro_02.wav": "El autor propone estudiar las sociedades junto con el ambiente que habitan. La organización social, la economía y la política están vinculadas a las tecnologías con las que transformamos los ecosistemas.",
    "intro_03.wav": "Por eso, la crisis ambiental no se resuelve únicamente con tecnología: también exige revisar cómo organizamos la sociedad.",
    "intro_04.wav": "La cultura es frágil porque sus soluciones pueden no ser suficientes para superar una crisis que hoy tiene alcance planetario.",
    "scene_01.wav": "Hace miles de años, pequeños grupos humanos recorrían el paisaje buscando agua, frutos y refugio. Cada desplazamiento dependía de conocer las señales del entorno.",
    "scene_02.wav": "La caza exigía observar huellas, elegir herramientas y coordinarse. No era una acción aislada: la cooperación y la comunicación aumentaban las posibilidades de sobrevivir.",
    "scene_03.wav": "Alrededor del fuego, el grupo encontraba calor y protección. Compartir alimentos y conocimientos fortalecía la vida colectiva.",
    "scene_04.wav": "La naturaleza ofrecía alimento, agua y refugio, pero también imponía límites. Comprender el territorio era esencial para evitar riesgos y mantener al grupo.",
    "scene_05.wav": "Con el tiempo, los grupos humanos perfeccionaron herramientas y aprendieron a aprovechar distintos recursos. La técnica amplió sus posibilidades de adaptación.",
    "scene_06.wav": "Golpear, tallar y dar forma a la piedra requería práctica. Las habilidades se compartían entre personas y generaciones, convirtiendo el aprendizaje en una ventaja colectiva.",
    "scene_07.wav": "La cooperación ayudaba a organizar la búsqueda de alimentos y a responder a los cambios del paisaje. La cultura no era solo una herramienta: también era conocimiento compartido.",
    "scene_08.wav": "Las técnicas más eficaces también podían aumentar la presión sobre las presas. Una innovación puede facilitar la supervivencia y, a la vez, transformar el equilibrio ecológico.",
    "scene_09.wav": "Algunas comunidades comenzaron a cuidar plantas y aprovechar sus ciclos. La obtención de alimentos dejó de depender únicamente de encontrar recursos silvestres.",
    "scene_10.wav": "La domesticación de animales y el cultivo favorecieron asentamientos más estables. Las personas construyeron viviendas y organizaron tareas para mantener a la comunidad.",
    "scene_11.wav": "Los campos y las viviendas modificaron el territorio. Al seleccionar las especies útiles, las sociedades también cambiaron qué plantas y animales podían prosperar cerca de ellas.",
    "scene_12.wav": "Una producción más estable favoreció el crecimiento y nuevas formas de trabajo, pero también generó nuevas presiones sobre el suelo y los ecosistemas. Toda transformación trae oportunidades y responsabilidades.",
}


def main() -> None:
    pending = {name: text for name, text in NARRATIONS.items() if not (VOICE_DIR / name).exists()}
    if not pending:
        print("Todas las narraciones ya existen; no hay nada que generar.")
        return

    # Importar Kokoro carga PyTorch, así que solo se hace si hay algo que generar.
    from kokoro import KPipeline

    pipeline = KPipeline(lang_code="e")  # "e" = español
    VOICE_DIR.mkdir(parents=True, exist_ok=True)
    for name, text in pending.items():
        chunks = [audio for _, _, audio in pipeline(text, voice=VOICE, speed=SPEED)]
        if not chunks:
            raise RuntimeError(f"Kokoro no generó audio para {name}")
        sf.write(VOICE_DIR / name, np.concatenate(chunks), SAMPLE_RATE)
        print(f"Generado: {name}")


if __name__ == "__main__":
    main()
