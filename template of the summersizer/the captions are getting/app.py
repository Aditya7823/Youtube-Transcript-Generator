from flask import Flask, render_template, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

def get_video_captions(video_id):
    """Fetch captions for a given YouTube video ID using youtube_transcript_api."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        captions = [{"text": entry["text"], "start": entry["start"], "duration": entry["duration"]} for entry in transcript]
        return captions
    except Exception as e:
        return None

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

if __name__ == "__main__":
    app.run(debug=True)
