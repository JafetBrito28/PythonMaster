import telegram
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
)
import logging

# Configuración del registro (logging) para depuración
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Token de tu bot (obtenido de BotFather)
TOKEN = '7333298550:AAEFkOxIAVRgoSsnfJqC1EZ3cTU5E_cfXGw'

# Diccionario para almacenar las tareas (se guarda en la nube de Telegram)
tareas = {}

# Estado para el ConversationHandler
AGREGAR_TAREA = 0

# Función para guardar las tareas en la nube
def guardar_tareas(update, context):
    """Guarda el diccionario de tareas en la bot_data (nube de Telegram)."""
    context.chat_data['tareas'] = tareas

# Función para cargar las tareas desde la nube
def cargar_tareas(update, context):
    """Carga el diccionario de tareas desde la bot_data (nube de Telegram)."""
    global tareas
    tareas = context.chat_data.get('tareas', {})

# Comando /start (mensaje de bienvenida y opciones)
async def start(update, context):
    """Envía un mensaje de bienvenida con las opciones disponibles al usuario."""
    cargar_tareas(update, context)
    mensaje = "Bienvenido a tu bot de tareas!\n\n"
    mensaje += "Opciones:\n"
    mensaje += "/agregar - Agregar una nueva tarea\n"
    mensaje += "/ver - Ver todas las tareas\n"
    mensaje += "/completar <número> - Marcar una tarea como completada\n"
    mensaje += "/eliminar <número> - Eliminar una tarea\n"
    await update.message.reply_text(mensaje)
   
# Comando /agregar (inicia el proceso para agregar una tarea)
async def agregar_command(update, context):
    await update.message.reply_text("Ingresa la nueva tarea:")
    return AGREGAR_TAREA

# Función para agregar la tarea (se ejecuta cuando el usuario ingresa texto)
async def agregar_tarea(update, context):
    """Agrega una nueva tarea a la lista."""
    cargar_tareas(update, context)
    texto_tarea = update.message.text  # Obtiene el texto de la tarea

    tareas[len(tareas) + 1] = {'texto': texto_tarea, 'completada': False}
    guardar_tareas(update, context)
    await update.message.reply_text(f"Tarea agregada: {texto_tarea}")
    return ConversationHandler.END

# Comando /agregar (manejador para mensajes nuevos y editados que contienen "/agregar")
async def agregar(update, context):
    """Agrega una nueva tarea a la lista si se proporciona texto junto con el comando."""
    cargar_tareas(update, context)
    texto_tarea = ' '.join(context.args)

    if texto_tarea:  # Si se proporciona texto junto con el comando, agregar la tarea
        tareas[len(tareas) + 1] = {'texto': texto_tarea, 'completada': False}
        guardar_tareas(update, context)
        await update.message.reply_text(f"Tarea agregada: {texto_tarea}")
    else:  # Si no se proporciona texto, iniciar el ConversationHandler
        await update.message.reply_text("Ingresa la nueva tarea:")
        return AGREGAR_TAREA

    return ConversationHandler.END  # Finalizar el ConversationHandler si se agregó la tarea

# Comando /ver (ver todas las tareas)
async def ver(update, context):
    """Muestra la lista de tareas al usuario."""
    cargar_tareas(update, context)
    if tareas:
        mensaje = "Tus tareas:\n\n"
        for num, tarea in tareas.items():
            estado = "✅" if tarea['completada'] else "❌"
            mensaje += f"{num}. {estado} {tarea['texto']}\n"  # Sin notas
        await update.message.reply_text(mensaje)
    else:
        await update.message.reply_text("No tienes tareas pendientes.")

# Comando /completar (marcar una tarea como completada)
async def completar(update, context):
    """Marca una tarea como completada."""
    cargar_tareas(update, context)
    try:
        num_tarea = int(context.args[0])
        if num_tarea in tareas:
            tareas[num_tarea]['completada'] = True
            guardar_tareas(update, context)
            await update.message.reply_text(f"Tarea {num_tarea} marcada como completada.")
        else:
            await update.message.reply_text("Número de tarea inválido.")
    except (IndexError, ValueError):
        await update.message.reply_text("Por favor, ingresa el número de tarea después del comando /completar")


# Comando /eliminar (eliminar una tarea)
async def eliminar(update, context):
    """Elimina una tarea de la lista."""
    cargar_tareas(update, context)
    try:
        num_tarea = int(context.args[0])
        if num_tarea in tareas:
            del tareas[num_tarea]
            guardar_tareas(update, context)
            await update.message.reply_text(f"Tarea {num_tarea} eliminada.")
        else:
            await update.message.reply_text("Número de tarea inválido.")
    except (IndexError, ValueError):
        await update.message.reply_text("Por favor, ingresa el número de tarea después del comando /eliminar")


# Error handler para manejar errores inesperados
async def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

# Crear la aplicación y obtener el updater
application = Application.builder().token(TOKEN).build()

# ConversationHandler para agregar tareas
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("agregar", agregar_command)],
    states={
        AGREGAR_TAREA: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, agregar_tarea),
        ],
    },
    fallbacks=[],
)

# Añadir los manejadores de comandos y el ConversationHandler
application.add_handler(conv_handler)
application.add_handler(CommandHandler('start', start))
application.add_handler(CommandHandler('ver', ver))
application.add_handler(CommandHandler('completar', completar))
application.add_handler(CommandHandler('eliminar', eliminar))
# Añadir manejador para el comando /agregar (mensajes nuevos y editados)
application.add_handler(CommandHandler('agregar', agregar))


# Error handler
application.add_error_handler(error)

# Iniciar el bot
application.run_polling()
