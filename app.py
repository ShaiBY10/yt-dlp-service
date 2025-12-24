from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import uuid
import os

app = FastAPI()

DOWNLOAD_DIR = "/downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

class DownloadRequest(BaseModel):
    url: str

@app.post("/download")
def download_video(req: DownloadRequest):
    video_id = str(uuid.uuid4())
    output_template = f"{DOWNLOAD_DIR}/{video_id}.%(ext)s"

    cmd = [
        "yt-dlp",
        "-f", "best",
        "-o", output_template,
        req.url
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise HTTPException(
            status_code=500,
            detail=result.stderr
        )

    return {
        "status": "ok",
        "video_id": video_id,
        "log": result.stdout
    }
