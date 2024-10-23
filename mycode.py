import os  # for creating directory (downloads) in user's system
import yt_dlp  # for downloading yt vids (specifically for yt and other sites)

def download_audio(url):
    output_temp = os.path.join('downloaded', '%(title)s.%(ext)s')  # for output file name (title) and (extension)

    ydl_opts = {
        'format': 'bestaudio/best',  # we will be choosing the best available audio
        'extractaudio': True,  # extracting audio only from video
        'outtmpl': output_temp,  # after extracting the audio, we have to name it according to the pre-defined template
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',  # using FFmpeg for extracting the audio
            'preferredcodec': 'mp3',  # preferred audio codec
            'preferredquality': '192',  # sound quality -> 192kbps
        }],
    }

    if not os.path.exists('downloaded'):  # if system doesn't have the directory 'downloaded'
        os.makedirs('downloaded')  # then create one

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])  # for downloading the specific file from the given URL

if __name__ == '__main__':
    # Get the YouTube video URL from user input
    youtube_url = input("Enter the YouTube video URL: ")
    
    try:
        download_audio(youtube_url)  # this is our download_audio function to download the audio
        print("Download completed!")
    except Exception as e:
        print(f"An error occurred: {e}")
