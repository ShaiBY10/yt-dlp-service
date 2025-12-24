"""
yt-dlp HTTP microservice.
POST /download { "url": "<instagram post url>" }
Returns raw MP4.
"""

import subprocess
import uuid
import os
from flask import Flask, request, send_file, jsonify

app = Flask(__name__)

DOWNLOAD_DIR = "/tmp/videos"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "Missing url"}), 400

    post_url = data["url"]
    filename = f"{uuid.uuid4()}.mp4"
    filepath = os.path.join(DOWNLOAD_DIR, filename)

    cmd = [
        "yt-dlp",
        "--no-playlist",
        "-f", "mp4",
        "-o", filepath,
        post_url,
    ]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        return jsonify({"error": "Download failed"}), 500

    return send_file(filepath, mimetype="video/mp4")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
