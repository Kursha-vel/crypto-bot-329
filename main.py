import os
from datetime import datetime, timedelta
from python_telegram_bot import BotCommand, Update, Message
from python_telegram_bot.telegram import ApplicationBuilder, ContextTypes, InlineKeyboardMarkup, ReplyKeyboardMarkup
import asyncio
from python_telegram_bot.exceptions import TelegramAPIError

TOKEN = os.environ.get("TELEGRAM_TOKEN")
API_URL = "https://api.coingecko.com/api/v3/simple/price"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Этот бот показывает курс Bitcoin и Ethereum каждые 12 часов.")

async def send_crypto_price(context: ContextTypes.DEFAULT_TYPE):
    try:
        response = await fetch_crypto_price()
        await context.bot.send_message(chat_id=context.job.chat_id, text=response)
    except TelegramAPIError as e:
        print(e)

async def fetch_crypto_price():
    import requests
    params = {"ids": "bitcoin,ethereum", "vs_currencies": "usd"}
    response = requests.get(API_URL, params=params).json()
    bitcoin_price = response["bitcoin"]["usd"]
    ethereum_price = response["ethereum"]["usd"]
    return f"Курс Bitcoin: ${bitcoin_price}\nКурс Ethereum: ${ethereum_price}"

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(BotCommand("start", start))
    job_queue = app.job_queue
    job_queue.run_repeating(send_crypto_price, interval=timedelta(hours=12), first=timedelta(seconds=1))
    app.run_polling(drop_pending_updates=True)
if __name__ == "__main__":
    main()