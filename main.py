from flask import Flask, request, jsonify, send_file
import subprocess
import os
import uuid

app = Flask(__name__)

@app.route("/extract-audio", methods=["POST"])
def extract_audio():
    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "Você precisa enviar a URL do vídeo"}), 400

    output_file = f"audio_{uuid.uuid4().hex}.mp3"
    try:
        # Baixa o vídeo e extrai apenas o áudio em mp3
        subprocess.run(
            ["yt-dlp", "-x", "--audio-format", "mp3", "-o", output_file, url],
            check=True
        )

        # Envia o arquivo de áudio extraído
        return send_file(output_file, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        # Remove o arquivo temporário após enviar
        if os.path.exists(output_file):
            os.remove(output_file)

@app.route("/", methods=["GET"])
def home():
    return "Servidor de extração de áudio está rodando!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
