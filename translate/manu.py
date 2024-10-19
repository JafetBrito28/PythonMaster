import translators as ts  # Usaremos esta librería para la traducción
import emoji  # Para añadir los emojis de la hoja de arce
from rich import print  # Para darle color a la salida en la terminal

# Emojis y bienvenida con estilo
print(f"[bold green]{emoji.emojize(':maple_leaf:') * 3} Bienvenido al Traductor Canadiense {emoji.emojize(':maple_leaf:') * 3}[/bold green]")

def modo_traduccion_directa():
    while True:
        texto = input("[bold blue]Ingresa el texto a traducir (o 'q' para salir): [/bold blue]")
        if texto.lower() == 'q':
            break

        idioma_destino = input("[bold blue]Idioma de destino (ej: 'es' para español): [/bold blue]")

        try:
            traduccion = ts.translate_text(texto, from_language='auto', to_language=idioma_destino)
            print(f"[bold yellow]Traducción:[/bold yellow] {traduccion}")
        except Exception as e:
            print(f"[bold red]Error en la traducción: {e}[/bold red]")

def modo_conversacion():
    idioma_usuario1 = input("[bold blue]Idioma del Usuario 1: [/bold blue]")
    idioma_usuario2 = input("[bold blue]Idioma del Usuario 2: [/bold blue]")

    while True:
        texto_usuario1 = input(f"[bold cyan]Usuario 1 ({idioma_usuario1}): [/bold cyan]")
        if texto_usuario1.lower() == 'q':
            break

        try:
            traduccion_usuario2 = ts.translate_text(texto_usuario1, from_language=idioma_usuario1, to_language=idioma_usuario2)
            print(f"[bold magenta]Usuario 2 ({idioma_usuario2}):[/bold magenta] {traduccion_usuario2}")
        except Exception as e:
            print(f"[bold red]Error en la traducción: {e}[/bold red]")

        # Aquí iría el código para obtener el texto del Usuario 2 y traducirlo para el Usuario 1 (similar al bloque anterior)

# Menú principal
while True:
    print("\n[bold underline]Selecciona un modo:[/bold underline]")
    print("1. Traducción Directa")
    print("2. Conversación")
    print("3. Salir")

    opcion = input("> ")
    if opcion == '1':
        modo_traduccion_directa()
    elif opcion == '2':
        modo_conversacion()
    elif opcion == '3':
        break
    else:
        print("[bold red]Opción inválida[/bold red]")
