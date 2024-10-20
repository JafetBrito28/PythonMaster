import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from gtts import gTTS

# Configuración del bot (reemplaza con tu token)
TOKEN = ''

# Configuración del logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="¡Hola! Soy tu bot conversor de texto a voz. Usa los siguientes comandos:\n\n/voz <texto> - Convierte el texto a audio\n/ayuda - Muestra este mensaje")

async def voz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args)  # Obtiene el texto después del comando /voz
    
    if not text:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Por favor, proporciona el texto que deseas convertir a audio después del comando /voz.")
        return

    # Convertir texto a audio con gTTS
    tts = gTTS(text, lang='es')
    tts.save("audio.mp3")

    # Enviar audio al usuario
    await context.bot.send_audio(chat_id=update.effective_chat.id, audio=open('audio.mp3', 'rb'))

async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Usa los siguientes comandos:\n\n/voz <texto> - Convierte el texto a audio\n/ayuda - Muestra este mensaje")

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    # Comandos y manejadores de mensajes
    start_handler = CommandHandler('start', start)
    voz_handler = CommandHandler('voz', voz)
    ayuda_handler = CommandHandler('ayuda', ayuda)

    application.add_handler(start_handler)
    application.add_handler(voz_handler)
    application.add_handler(ayuda_handler)

    # Iniciar el bot
    application.run_polling()

if __name__ == '__main__':
    main()
