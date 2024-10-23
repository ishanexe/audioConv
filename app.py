from flask import Flask, render_template, request, send_from_directory
import os
import yt_dlp

app = Flask(__name__)

# Function to download audio from a YouTube video
def download_audio(url):
    output_temp = os.path.join('downloaded', '%(title)s.%(ext)s')  # Output file template
    ydl_opts = {
        'format': 'bestaudio/best',  # Choose the best available audio
        'extractaudio': True,  # Extract audio only
        'outtmpl': output_temp,  # Output file naming template
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',  # Use FFmpeg to extract audio
            'preferredcodec': 'mp3',  # Convert to mp3
            'preferredquality': '192',  # Audio quality
        }],
    }

    # Create 'downloaded' directory if it doesn't exist
    if not os.path.exists('downloaded'):
        os.makedirs('downloaded')

    # Download audio
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

@app.route('/', methods=['GET', 'POST'])
def index():
    success = False
    error = None
    filename = None  # To store the name of the downloaded file

    if request.method == 'POST':
        youtube_url = request.form['youtube_url']  # Get the YouTube URL from the form
        try:
            download_audio(youtube_url)  # Download the audio
            # Get the name of the first downloaded file
            filename = os.listdir('downloaded')[0]  
            success = True  # Set success flag to True
        except Exception as e:
            error = str(e)  # Capture any errors

    # Render the template and pass success, error, and filename if applicable
    return render_template('index.html', success=success, error=error, filename=filename)

@app.route('/downloaded/<path:filename>')
def download_file(filename):
    # Send the file for download, triggering a download on the client side
    return send_from_directory('downloaded', filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
