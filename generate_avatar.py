import os
import requests
import time
import json
import cv2
import numpy as np
from dotenv import load_dotenv

# Load API Key from .env file
load_dotenv()
HEYGEN_API_KEY = os.getenv("HEYGEN_API_KEY")

# HeyGen API URLs
CREATE_VIDEO_URL = "https://api.heygen.com/v1/video/generate"  # URL to create the video
GET_VIDEO_STATUS_URL = "https://api.heygen.com/v1/video/status"  # URL to check video status
DOWNLOAD_VIDEO_URL = "https://api.heygen.com/v1/video/download"  # URL to download video (if needed)

# Function to generate avatar video
def generate_avatar_video(text, language="en"):
    # Choose voice based on language
    voice_id = "en-US-JennyNeural" if language == "en" else "hi-IN-MadhurNeural"
    headers = {
        "Authorization": "Bearer " + HEYGEN_API_KEY,
        "Content-Type": "application/json"
    }


    # Use your actual avatar ID here
    avatar_id = "Annie_expressive_public"  # Updated avatar ID

    payload = {
        "script": {"type": "text", "input": text},
        "voice": {"language": language, "voice_id": voice_id},
        "avatar_id": avatar_id,  # Updated avatar ID
    }

    response = requests.post(CREATE_VIDEO_URL, headers=headers, json=payload)
    result = response.json()

    if response.status_code == 200 and "video_id" in result:
        return result["video_id"]
    else:
        print("Error:", result)
        return None

# Function to check video status
def check_video_status(video_id):
    headers = {"Authorization": f"Bearer {HEYGEN_API_KEY}"}

    while True:
        response = requests.get(f"{GET_VIDEO_STATUS_URL}/{video_id}", headers=headers)
        result = response.json()

        if result.get("status") == "completed":
            return result["video_url"]
        elif result.get("status") == "failed":
            print("Error: Video generation failed.")
            return None
        time.sleep(5)  # Wait 5 seconds before checking again

# Function to download video
def save_video(video_url, filename="generated_avatar.mp4"):
    response = requests.get(video_url)

    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"✅ Video saved as {filename}")
        return filename
    else:
        print("❌ Failed to download video.")
        return None

# Function to play video
def play_video(filename):
    cap = cv2.VideoCapture(filename)

    if not cap.isOpened():
        print("Error: Unable to open video file.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Generated Avatar", frame)
        if cv2.waitKey(25) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

# Get user input
text = input("Enter the text: ")
language = input("Enter language (en/hi): ")

video_id = generate_avatar_video(text, language)
if video_id:
    print("⏳ Waiting for video to generate...")
    video_url = check_video_status(video_id)
    if video_url:
        video_file = save_video(video_url)
        if video_file:
            print("🎬 Playing video...")
            play_video(video_file)
