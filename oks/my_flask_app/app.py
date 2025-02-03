import os
from flask import Flask, render_template, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import google.genai as genai  # Importing the genai library

# Initialize Flask app
app = Flask(__name__)

# Setup Gemini API key
GEMINI_API_KEY = 'AIzaSyCHiv4DhQa6EjXlv8O-Zeh_OArCMRUfWjE'  # Replace with your actual Gemini API key

# Function to fetch captions for a given YouTube video ID using youtube_transcript_api
def get_video_captions(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        captions = [{"text": entry["text"], "start": entry["start"], "duration": entry["duration"]} for entry in transcript]
        return captions
    except Exception as e:
        return None

# Function to summarize text (captions) using Google Gemini API
def summarize_text(captions):
    prompt = " ".join([entry["text"] for entry in captions])  # Create a prompt string from captions

    try:
        # Initialize the Gemini client with the API key
        client = genai.Client(api_key=GEMINI_API_KEY)

        # Generate content using the 'gemini-2.0-flash' model
        response = client.models.generate_content(
            model="gemini-1.5-flash", contents=prompt + " Give me notes from this."
        )

        # Return the response text
        return response.text
    except Exception as e:
        print(f"Error generating content: {e}")
        return "Failed to generate content."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_captions", methods=["POST"])
def get_captions():
    video_url = request.form["video_url"]
    video_id = video_url.split("v=")[-1].split("&")[0]  # Extract video ID safely

    captions = get_video_captions(video_id)

    if not captions:
        return jsonify({"error": "Captions not available for this video."})

    return jsonify({"captions": captions})

@app.route("/get_notes", methods=["POST"])
def get_notes():
    video_url = request.form["video_url"]
    video_id = video_url.split("v=")[-1].split("&")[0]  # Extract video ID safely

    captions = get_video_captions(video_id)

    if not captions:
        return jsonify({"error": "Captions not available for this video."})

    # Generate notes by summarizing captions using the summarize_text function
    notes = summarize_text(captions)

    return jsonify({"notes": notes})

if __name__ == "__main__":
    app.run(debug=True)
