import asyncio
import edge_tts
import re
import os
import pygame

# Initialize pygame mixer once
pygame.mixer.init()

WHISPER_THOUGHTS = False  # Set to False to skip thoughts completely

async def _generate_audio(text, voice, filename, rate="+0%", pitch="+0Hz"):
    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=rate,
        pitch=pitch
    )
    with open(filename, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])

async def _play_audio(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        await asyncio.sleep(0.1)
    pygame.mixer.music.unload()
    os.remove(file)

async def _speak(text):
    # Split out <think>...</think> sections
    parts = re.split(r"(<think>.*?</think>)", text, flags=re.DOTALL)

    for i, part in enumerate(parts):
        if not part.strip():
            continue

        if part.startswith("<think>") and part.endswith("</think>"):
            thought = re.sub(r"</?think>", "", part).strip()
            if WHISPER_THOUGHTS and thought:
                filename = f"thought_{i}.mp3"
                await _generate_audio(
                    thought,
                    voice="en-US-JennyNeural",
                    filename=filename,
                    rate="-30%",
                    pitch="-10Hz"
                )
                await _play_audio(filename)
        else:
            normal = re.sub(r"<.*?>", "", part).strip()
            if normal:
                filename = f"speech_{i}.mp3"
                await _generate_audio(
                    normal,
                    voice="en-US-JennyNeural",
                    filename=filename,
                    rate="+0%",
                    pitch="+0Hz"
                )
                await _play_audio(filename)

def speak(text):
    asyncio.run(_speak(text))
