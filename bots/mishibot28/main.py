import asyncio
import logging
import re
import telegram
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import pytube
from pytube import YouTube

# Token de tu bot de Telegram
TOKEN = ''

# Configuración del logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Monkey Patch para PyTube
def apply_descrambler(stream_manifest, video_id):
    """Apply various in-place transforms to YouTube's media stream data."""
    for i, stream_data in enumerate(stream_manifest):
        stream_data["url"] = pytube.cipher.get_streaming_url(
            video_id,
            stream_data["s"],
            pytube.__js__,
        )
        stream_manifest[i] = stream_data

pytube.StreamQuery.descramble = apply_descrambler

# Función de inicio del bot
async def start(update, context):
    logger.info("Entrando en la función start")
    await update.message.reply_text('¡Hola! Soy pytube28bot. Envíame un enlace de YouTube para descargar el audio.')

# Función para descargar audio (con expresión regular mejorada)
async def download_audio(update, context):
    logger.info("Entrando en la función download_audio")
    try:
        url = update.message.text

        # Validación del enlace de YouTube (más flexible)
        if not re.match(r'^(https?\:\/\/)?(www\.|m\.)?(youtube\.com|youtu\.?be)\/.+$', url):
            await update.message.reply_text('Por favor, envía un enlace válido de YouTube.')
            return

        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        stream.download(filename=f"{yt.title}.mp4")
        await context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(f"{yt.title}.mp4", 'rb'))
    except Exception as e:
        logger.error(f"Error en download_audio: {e}")
        await update.message.reply_text(f'Error: {e}')

# Función de ayuda
async def help(update, context):
    logger.info("Entrando en la función help")
    await update.message.reply_text('Envía un enlace de YouTube para descargar el audio. Usa /download para descargar y /about para información.')

# Función "acerca de"
async def about(update, context):
    logger.info("Entrando en la función about")
    await update.message.reply_text('Soy pytube28bot, creado para descargar audio de YouTube. ¡Disfruta!')

# Manejador de errores
async def error_handler(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

# Crear la aplicación
application = Application.builder().token(TOKEN).build()

# Agregar manejadores
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("download", download_audio))
application.add_handler(CommandHandler("help", help))
application.add_handler(CommandHandler("about", about))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_audio))
application.add_error_handler(error_handler)

# Iniciar el bot
if __name__ == '__main__':
    application.run_polling()
