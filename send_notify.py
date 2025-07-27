import asyncio
import os
from aiogram import Bot
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise ValueError("API_TOKEN is not set в .env")

# Укажите Telegram ID получателя здесь:
TARGET_USER_ID = 123456789  # <-- замените на нужный ID

async def send_notify():
    bot = Bot(token=API_TOKEN)
    await bot.delete_webhook()  # Удаляем вебхук перед отправкой сообщения
    await bot.send_message(TARGET_USER_ID, "🔔 Уведомление: Второй тур скоро начнётся!")
    await bot.session.close()

if __name__ == "__main__":
    asyncio.run(send_notify())