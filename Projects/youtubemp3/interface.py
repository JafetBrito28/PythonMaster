import tkinter as tk
from tkinter import filedialog 
import os
import pytube  

def download_youtube_mp3(video_url, download_path):
    try:
        youtube_video = pytube.YouTube(video_url)
        audio_stream = youtube_video.streams.filter(only_audio=True).first()
        output_file = audio_stream.download(output_path=download_path) 
        base, ext = os.path.splitext(output_file)
        new_file = base + '.mp3'
        os.rename(output_file, new_file)
        return f"MP3 file downloaded successfully: {new_file}"

    except Exception as e:
        return f"An error occurred while downloading: {e}"

# Tkinter GUI Setup
window = tk.Tk()
window.title("YouTube MP3 Downloader")

tk.Label(window, text="Enter YouTube URL:").pack()
url_entry = tk.Entry(window, width=40)
url_entry.pack()

def download_video():
    video_url = url_entry.get()
    download_path = filedialog.askdirectory()  
    if video_url and download_path:  
        result = download_youtube_mp3(video_url, download_path)
        status_label.config(text=result)
    else:
        status_label.config(text="Please fill all fields", fg="red")     

tk.Button(window, text="Download", command=download_video).pack()

status_label = tk.Label(window, text="")
status_label.pack()

window.mainloop()

