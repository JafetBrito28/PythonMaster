import pytube
import os  

def download_youtube_mp3(video_url):
    try:
        youtube_video = pytube.YouTube(video_url)
        audio_stream = youtube_video.streams.filter(only_audio=True).first()
        output_file = audio_stream.download(output_path='./')  # Download to current folder
        base, ext = os.path.splitext(output_file)
        new_file = base + '.mp3'
        os.rename(output_file, new_file)
        print(f"MP3 file downloaded successfully: {new_file}")

    except Exception as e:
        print(f"An error occurred while downloading: {e}")

# Example usage:
video_url = "https://www.youtube.com/watch?v=N1_A7RnyL7I"  # Replace with your video URL
download_youtube_mp3(video_url)