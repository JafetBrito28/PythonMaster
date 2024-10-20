import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, filters
import asyncio
from asyncio import Queue

# Token de tu bot (reemplaza con el tuyo)
TOKEN = '6470198650:AAF40CCkm7cc2BuAjlYyPBj3DfX0axzAZnc'
update_queue = Queue()  # Crea una cola para las actualizaciones

# Lista de preguntas y respuestas
preguntas = [
    {
        'pregunta': '¿Cuál es la capital de Francia?',
        'respuesta': 'París'
    },
    {
        'pregunta': '¿Quién pintó la Mona Lisa?',
        'respuesta': 'Leonardo da Vinci'
    },
    # Agrega más preguntas aquí...
]

puntuacion = {}  # Diccionario para almacenar la puntuación de cada usuario

# Función para iniciar la trivia
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="¡Bienvenido a la trivia! Responde las preguntas correctamente para ganar puntos.")
    hacer_pregunta(update, context)

# Función para hacer una pregunta
def hacer_pregunta(update, context):
    pregunta = preguntas.pop(0)  # Toma la primera pregunta de la lista
    context.user_data['respuesta_correcta'] = pregunta['respuesta']
    context.bot.send_message(chat_id=update.effective_chat.id, text=pregunta['pregunta'])

# Función para verificar la respuesta
def verificar_respuesta(update, context):
    respuesta_usuario = update.message.text.lower()  # Convertimos la respuesta a minúsculas
    respuesta_correcta = context.user_data['respuesta_correcta'].lower()

    if respuesta_usuario == respuesta_correcta:
        context.bot.send_message(chat_id=update.effective_chat.id, text="¡Correcto! Ganaste un punto.")
        puntuacion[update.effective_user.id] = puntuacion.get(update.effective_user.id, 0) + 1
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Incorrecto. La respuesta correcta era: {respuesta_correcta}")

    if preguntas:  # Si quedan preguntas, hacemos otra
        hacer_pregunta(update, context)
    else:  # Si no quedan preguntas, mostramos la puntuación final
        context.bot.send_message(chat_id=update.effective_chat.id, text="¡Fin de la trivia!")
        for usuario, puntos in puntuacion.items():
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"{usuario.first_name}: {puntos} puntos")

# Configuración del updater y dispatcher
updater = Updater(TOKEN, update_queue=update_queue) # Se añade la cola de actualizaciones 
dispatcher = updater.dispatcher

# Añadir los manejadores
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), verificar_respuesta))

# Iniciar el bot
updater.start_polling()