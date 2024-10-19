import tkinter as tk
from tkinter import ttk, filedialog
import os
import re
import pytube
from pytube.exceptions import VideoUnavailable, PytubeError
from PIL import Image, ImageTk

# Configuración de la ventana principal
window = tk.Tk()
window.title("YouTube MP3 Downloader by H4SH")
window.configure(bg="black")  # Fondo negro

# Estilo visual
style = ttk.Style()
style.configure("TLabel", font=("Courier", 12), background="black", foreground="red")
style.configure("TButton", font=("Courier", 12, "bold"), padding=10, background="white", foreground="red")
style.configure("Success.TLabel", font=("Courier", 12), background="black", foreground="green")  # Estilo éxito
style.configure("Error.TLabel", font=("Courier", 12), background="black", foreground="red")  # Estilo error
style.configure("Url.TEntry", font=("Courier", 12), background="white", foreground="black")  # Fondo blanco, texto negro

# Título (25% más grande)
title_label = ttk.Label(window, text="H4SHM4LWAR3", justify="center")
title_label.config(font=("Courier", 18, "bold"))  # Aumento del tamaño de fuente
title_label.pack(pady=10)

# Frase en varios idiomas (subtítulo)
subtitle_label = ttk.Label(window, text="Hack the planet, Pirater la planète, Hackera il pianeta, Hackea el planeta", justify="center")
subtitle_label.pack()

# Carga y redimensiona la imagen
logo_image = Image.open("./foto.png")
resized_image = logo_image.resize((350, 350))
logo_photo = ImageTk.PhotoImage(resized_image)

# Etiqueta de imagen
image_label = ttk.Label(window, image=logo_photo)
image_label.pack(pady=20)

# Campos de entrada
url_frame = ttk.Frame(window)
url_frame.pack(pady=10)
ttk.Label(url_frame, text="Enter YouTube URL:").pack(side="left")
url_entry = ttk.Entry(url_frame, width=40, style="Url.TEntry")  # Aplicar el estilo específico
url_entry.pack(side="left")

# Función para validar la URL de YouTube
def is_valid_url(url):
    youtube_regex = re.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+')
    return re.match(youtube_regex, url) is not None

# Función de descarga de YouTube en formato MP3
def download_youtube_mp3(video_url, download_path):
    try:
        youtube_video = pytube.YouTube(video_url)
        audio_stream = youtube_video.streams.filter(only_audio=True).first()
        output_file = audio_stream.download(output_path=download_path)
        base, ext = os.path.splitext(output_file)
        new_file = base + '.mp3'
        if not os.path.exists(new_file):
            os.rename(output_file, new_file)
        else:
            return f"File already exists: {new_file}"
        return f"MP3 downloaded successfully: {new_file}"
    
    except VideoUnavailable:
        return "Error: The video is unavailable. Please check the URL."
    
    except PytubeError as e:
        return f"Error with Pytube: {e}"
    
    except Exception as e:
        print(f"Error downloading video: {str(e)}")
        return f"Unexpected error: {e}"

# Función de descarga (mejorada para recordar la última carpeta)
def download_video():
    global download_path
    video_url = url_entry.get()

    if not is_valid_url(video_url):
        status_label.config(text="Invalid YouTube URL.", style="Error.TLabel")
        return

    if video_url and download_path:
        result = download_youtube_mp3(video_url, download_path)
        style_to_use = "Success.TLabel" if "successfully" in result else "Error.TLabel"
        status_label.config(text=result, style=style_to_use)
    else:
        status_label.config(text="Please enter the URL and select a folder.", style="Error.TLabel")

# Botón para seleccionar carpeta y variable para almacenar la ruta
download_path = ""
def select_download_path():
    global download_path
    download_path = filedialog.askdirectory()
    if download_path:
        status_label.config(text=f"Folder selected: {download_path}", style="Success.TLabel")
    else:
        status_label.config(text="Please select a folder.", style="Error.TLabel")

select_button = ttk.Button(window, text="Select Folder", command=select_download_path)
select_button.pack(pady=10)

# Botón de descarga
download_button = ttk.Button(window, text="Download", command=download_video)
download_button.pack()

# Etiqueta de estado
status_label = ttk.Label(window, text="", style="TLabel")
status_label.pack(pady=10)

# Botón "About Us"
def show_about():
    about_window = tk.Toplevel(window)
    about_window.title("About Us")
    about_label = ttk.Label(about_window, text="Choose Hack...")
    about_label.pack(padx=20, pady=20)
    about_window.configure(bg="black")  # Fondo negro para la ventana "About Us"

about_button = ttk.Button(window, text="About Us", command=show_about)
about_button.pack(pady=10)

window.mainloop()
