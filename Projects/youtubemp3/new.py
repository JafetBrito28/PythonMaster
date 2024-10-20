import tkinter as tk
from tkinter import ttk, filedialog
import os
import pytube
from PIL import Image, ImageTk

# Configuración de la ventana principal
window = tk.Tk()
window.title("YouTube MP3 Downloader")

# Carga y redimensiona la imagen
logo_image = Image.open("./foto.png")
resized_image = logo_image.resize((350, 350))
logo_photo = ImageTk.PhotoImage(resized_image)

# Estilo visual
style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 12))
style.configure("TButton", font=("Helvetica", 12, "bold"), padding=10)
style.configure("TEntry", font=("Helvetica", 12))

# Etiqueta de imagen
image_label = ttk.Label(window, image=logo_photo)
image_label.pack(pady=20)

# Campos de entrada
url_frame = ttk.Frame(window)
url_frame.pack(pady=10)
ttk.Label(url_frame, text="Ingrese la URL de YouTube:").pack(side="left")
url_entry = ttk.Entry(url_frame, width=40)
url_entry.pack(side="left")

# Botón para seleccionar carpeta y variable para almacenar la ruta
download_path = ""
def select_download_path():
    global download_path
    download_path = filedialog.askdirectory()
    if download_path:
        status_label.config(text=f"Carpeta seleccionada: {download_path}")
    else:
        status_label.config(text="Por favor, seleccione una carpeta.", fg="red")
select_button = ttk.Button(window, text="Seleccionar Carpeta", command=select_download_path)
select_button.pack(pady=10)

# Función de descarga
def download_youtube_mp3(video_url, download_path):
    try:
        youtube_video = pytube.YouTube(video_url)
        audio_stream = youtube_video.streams.filter(only_audio=True).first()
        output_file = audio_stream.download(output_path=download_path)
        base, ext = os.path.splitext(output_file)
        new_file = base + '.mp3'
        os.rename(output_file, new_file)
        return f"MP3 descargado correctamente: {new_file}"
    except Exception as e:
        return f"Error al descargar: {e}"

# Función de descarga (mejorada para recordar la última carpeta)
def download_video():
    global download_path
    video_url = url_entry.get()
    if video_url and download_path:
        result = download_youtube_mp3(video_url, download_path)
        status_label.config(text=result)
    else:
        status_label.config(text="Por favor, complete la URL y seleccione una carpeta.", fg="red")

# Botón de descarga
download_button = ttk.Button(window, text="Descargar", command=download_video)
download_button.pack()

# Etiqueta de estado
status_label = ttk.Label(window, text="")
status_label.pack(pady=10)

window.mainloop()
