"""
Usage
python split_video.py video.mp4 chapters.csv
output: chapters + clips/

"""
import csv
import subprocess
import os
import re
import sys

video = sys.argv[1]
csv_file = sys.argv[2]
output_dir = "clips"

output_dir = os.path.splitext(os.path.basename(csv_file))[0] + "_clips"
os.makedirs(output_dir, exist_ok=True)

def to_seconds(timestamp):
    parts = list(map(int, timestamp.split(":")))
    if len(parts) == 2:
        return parts[0] * 60 + parts[1]
    return parts[0] * 3600 + parts[1] * 60 + parts[2]

with open(csv_file, newline="", encoding="utf-8-sig") as f:
    chapters = list(csv.DictReader(f))

for i, chapter in enumerate(chapters):
    start = to_seconds(chapter["timestamp"])
    end = (
        to_seconds(chapters[i + 1]["timestamp"])
        if i + 1 < len(chapters)
        else None
    )

    title = re.sub(r'[<>:"/\\|?*]', "", chapter["title"])
    output = os.path.join(output_dir, f"{i + 1:03d} - {title}.mp4")

    command = ["ffmpeg", "-y", "-ss", str(start), "-i", video]
    if end is not None:
        command += ["-t", str(end - start)]

    command += ["-c:v", "libx264", "-c:a", "aac", output]

    subprocess.run(command, check=True)
    print(f"Created: {output}")
