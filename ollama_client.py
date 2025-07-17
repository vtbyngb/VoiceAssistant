import requests
import json

model_Name = "deepseek-r1:1.5b"

def ask_ollama(prompt, model=f"{model_Name}"):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt},
            stream=True
        )

        result = ""
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))
                if "response" in data:
                    result += data["response"]

        return result.strip() if result else "No response from model."
    except Exception as e:
        return f"Error connecting to Ollama: {e}"
