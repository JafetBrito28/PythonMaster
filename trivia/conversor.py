import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import requests

# Token de tu bot (reemplaza con el tuyo)
TOKEN = '7475862399:AAG80zTS2_EnG14Cv6QTNZZtg0FFu6DP4w4'

# Configuración del logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Función para obtener el tipo de cambio actual
async def obtener_tipo_cambio():
    url = "https://api.exchangerate-api.com/v4/latest/MXN"  # API de tipo de cambio
    response = requests.get(url)
    data = response.json()
    return data["rates"]["CAD"]

# Función para manejar el comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="¡Hola! Soy tu bot de conversión de moneda. Usa los siguientes comandos:\n/mxn_a_cad <cantidad> - Convierte pesos mexicanos a dólares canadienses\n/cad_a_mxn <cantidad> - Convierte dólares canadienses a pesos mexicanos")

# Función para manejar el comando /mxn_a_cad
async def mxn_a_cad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        cantidad = float(context.args[0])
        tipo_cambio = await obtener_tipo_cambio()
        cad = cantidad * tipo_cambio
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{cantidad} MXN son {cad:.2f} CAD")
    except (IndexError, ValueError):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Por favor, ingresa una cantidad válida (ejemplo: /mxn_a_cad 100)")

# Función para manejar el comando /cad_a_mxn
async def cad_a_mxn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        cantidad = float(context.args[0])
        tipo_cambio = await obtener_tipo_cambio()
        mxn = cantidad / tipo_cambio
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{cantidad} CAD son {mxn:.2f} MXN")
    except (IndexError, ValueError):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Por favor, ingresa una cantidad válida (ejemplo: /cad_a_mxn 50)")

# Función principal para iniciar el bot
def main():
    application = ApplicationBuilder().token(TOKEN).build()

    # Añadir manejadores de comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("mxn_a_cad", mxn_a_cad))
    application.add_handler(CommandHandler("cad_a_mxn", cad_a_mxn))

    # Iniciar el bot
    application.run_polling()

if __name__ == '__main__':
    main()
