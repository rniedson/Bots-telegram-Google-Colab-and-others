!pip install python-telegram-bot nest_asyncio

import nest_asyncio
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import datetime
import logging

# Token do bot fornecido pelo BotFather
TOKEN = 'your-key'

# Aplicar patch para permitir o uso do asyncio no Google Colab
nest_asyncio.apply()

# Configurar o log para depuração
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Comando /start recebido")
    await update.message.reply_text('Olá! Envie /hora para saber a hora atual.')

async def hora(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Comando /hora recebido")
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    await update.message.reply_text(f'A hora atual é {current_time}')

async def main() -> None:
    logger.info("Inicializando o bot")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hora", hora))

    logger.info("Iniciando o polling")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    
    # Manter o bot em execução
    logger.info("Bot está em execução, aguardando comandos...")
    await asyncio.Future()  # Manter o bot rodando

# Encerrar qualquer instância anterior do asyncio
try:
    loop = asyncio.get_running_loop()
    for task in asyncio.all_tasks(loop):
        task.cancel()
    loop.stop()
    loop.run_forever()
    loop.close()
except:
    pass

logger.info("Executando o bot")
asyncio.run(main())