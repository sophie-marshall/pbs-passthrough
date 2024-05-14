from flask import Flask, render_template, send_from_directory
import os
import pandas as pd 

app = Flask(__name__)

# Define the directory where your videos are stored
VIDEO_DIRECTORY = 'videos'
DATA_DIRECTORY = "data"


@app.route('/')
def index():
    # Get the list of video files in the directory
    video_files = [f for f in os.listdir(VIDEO_DIRECTORY) if os.path.isfile(os.path.join(VIDEO_DIRECTORY, f))]
    return render_template('index.html', video_files=video_files)

@app.route('/play/<filename>')
def play(filename):
    # Render the template for playing a video
    return render_template('play.html', filename=filename)

@app.route('/video/<filename>')
def video(filename):
    # Serve the video file
    return send_from_directory(VIDEO_DIRECTORY, filename)

@app.route("/data/<filename>")
def data(filename):
    return send_from_directory(DATA_DIRECTORY, filename)

if __name__ == '__main__':
    app.run(debug=True)
