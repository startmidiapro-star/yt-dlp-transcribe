from flask import Flask, request, jsonify
import subprocess
import whisper
import os

app = Flask(__name__)

# Carrega o modelo Whisper
model = whisper.load_model("base")

@app.route("/transcribe", methods=["POST"])
def transcribe():
    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "Você precisa enviar a URL do vídeo"}), 400

    try:
        # Baixa o vídeo usando yt-dlp
        output_file = "audio.mp3"
        subprocess.run(["yt-dlp", "-x", "--audio-format", "mp3", "-o", output_file, url], check=True)

        # Transcreve com Whisper
        result = model.transcribe(output_file, language="pt")
        os.remove(output_file)

        return jsonify({"transcription": result["text"]})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return "Servidor yt-dlp-transcribe está rodando!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
