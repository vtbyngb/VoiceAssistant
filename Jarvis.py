from modules.voice_input import listen_and_transcribe
from modules.tts_output import speak
from modules.ollama_client import ask_ollama
from modules.memory import remember, recall

def process_command(command):
    command = command.lower()

    if "remember that" in command:
        # Remember my birthday is on september
        parts = command.split("remember that", 1)[1].strip()
        if " is " in parts:
            key, value = parts.split(" is ", 1)
            remember(key.strip, value.strip)
            return f"Okay I'll Remember That {key.strip()} is {value.strip()}"
        else:
            return "I didn't Catch what I should remember."
    elif "what is" in command or "what's" in command:
        key = command.replace("what is", "").replace("what's", "").strip()
        value = recall(key)
        if value:
            return f"{key} is {value}."
        else:
            return f"I don't know what {key} is yet."
    return ask_ollama(command)


def main():
    print("Jarvis is listening... say something.")

    while True:
        text = listen_and_transcribe()
        if text:
            print(f"you said: {text}")
            response = ask_ollama(text)
            print(f"Jarvis: {response}")
            speak(response)


if __name__ == "__main__":
    main()
