from flask import Flask, request, jsonify
import subprocess
import whisper
import os
import uuid

app = Flask(__name__)

# Carrega o modelo Whisper (menor para economizar memória)
model = whisper.load_model("tiny")

@app.route("/transcribe", methods=["POST"])
def transcribe():
    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "Você precisa enviar a URL do vídeo"}), 400

    output_file = f"audio_{uuid.uuid4().hex}.mp3"
    try:
        # Baixa o vídeo usando yt-dlp
        subprocess.run(["yt-dlp", "-x", "--audio-format", "mp3", "-o", output_file, url], check=True)

        # Transcreve com Whisper
        result = model.transcribe(output_file, language="pt")
        return jsonify({"transcription": result["text"]})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        # Remove o arquivo temporário, se existir
        if os.path.exists(output_file):
            os.remove(output_file)

@app.route("/", methods=["GET"])
def home():
    return "Servidor yt-dlp-transcribe está rodando!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
