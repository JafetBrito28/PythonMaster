import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# Token de tu bot (reemplaza con el tuyo)
TOKEN = '7367251720:AAFgMAcMh1IKMM3P7_8PYtrrcL3PsuNfsv8'

# Configura el logging para ver mensajes de depuración en la consola
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Función para manejar el comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="¡Hola! Soy tu bot. Usa /hola para saludarme.")

# Función para manejar el comando /hola
async def hola(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="¡Hola! ¡Es un gusto saludarte!")

# Función principal para iniciar el bot
def main():
    # Crear el objeto Application (sin proxy)
    application = ApplicationBuilder().token(TOKEN).build()

    # Añadir manejadores de comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("hola", hola))

    # Iniciar el bot
    application.run_polling()

# Punto de entrada del script
if __name__ == '__main__':
    main()
