# modules/voice_input.py
import queue
import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
import time

model = WhisperModel("base", device="cpu", compute_type="int8")

sample_rate = 16000
block_duration = 0.5  # 0.5 second chunks
block_size = int(sample_rate * block_duration)
silence_threshold = 0.01  # tweak this if needed
max_silence_seconds = 2.5  # stop after this much silence, 1.5 last time, 5.5

q = queue.Queue()

def callback(indata, frames, time_info, status):
    if status:
        print("⚠️", status)
    q.put(indata.copy())

def listen_and_transcribe():
    print("Jarvis is listening... speak when ready.")

    audio_buffer = []
    silence_start = None

    try:
        with sd.InputStream(samplerate=sample_rate, channels=1, dtype="int16", callback=callback, blocksize=block_size):
            while True:
                chunk = q.get()
                audio = chunk.flatten().astype(np.float32) / 32768.0
                audio_buffer.append(audio)

                volume = np.abs(audio).mean()

                if volume < silence_threshold:
                    if silence_start is None:
                        silence_start = time.time()
                    elif time.time() - silence_start > max_silence_seconds:
                        break
                else:
                    silence_start = None

    except KeyboardInterrupt:
        print("Interrupted.")
        return None

    full_audio = np.concatenate(audio_buffer)
    print("Transcribing...")

    segments, _ = model.transcribe(full_audio, language="en")
    full_text = " ".join([seg.text.strip() for seg in segments]).strip()
    print(f"Final transcription: {full_text}")
    return full_text
