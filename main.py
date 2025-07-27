import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
import os
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db import init_db, add_user

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise ValueError("API_TOKEN is not set in the environment variables.")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

init_db()  # Инициализация базы данных

@dp.message(Command("start"))
async def start_command(message: types.Message):
    add_user(message.from_user.id)  # Сохраняем ID пользователя
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Заполнить Google форму",
        url="https://docs.google.com/forms/d/e/1FAIpQLScrw5LecmZ7FRUYhaKkk_VEE68kNtEANsmQiQAGD0rw3CIP7A/viewform"
    ))
    await message.answer(
        f"<b>👋 Привет!</b>\n\n"
        "<b>Это 1 тур отбора в группу по программированию.</b>\n\n"
        "Здесь я <b>не оцениваю ваши умственные способности</b>, а смотрю на <b>навыки</b>, <b>подходы к решению задач</b> и <b>желание учиться</b>.\n\n"
        "<b>Кому этот курс НЕ подходит:</b>\n"
        "1️⃣ <b>Кто не готов к сильным нагрузкам на протяжении полугода.</b>\n"
        "2️⃣ <b>Ленивым, безответственным, недисциплинированным и грубым.</b>\n"
        "3️⃣ <b>Тем, кто хочет просто попробовать себя в этой сфере.</b> Вы подаетесь, если <b>точно знаете, что хотите стать программистом высокого уровня.</b>\n"
        "4️⃣ <b>Не знающим русский и английский на базовом уровне.</b>\n\n"
        "<b>Ваша задача:</b>\n"
        f"— <b>Ваш Telegram ID:</b> <code>{message.from_user.id}</code>\n"
        "— <b>Скопируйте его и вставьте в Google Docs (ссылка ниже)</b>\n"
        "— <b>Заполнение займет 5-10 минут</b>\n\n"
        "<b>После прохождения первого тура вам придет уведомление о созвоне.</b>\n"
        "<b>Конец отбора: 24.07.25! Успейте заполнить форму, чтобы участвовать в отборе.</b>",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

# ...остальные обработчики...

async def main():
    print("Bot is running...")
    await bot.delete_webhook()  # Удаляем вебхук перед polling
    
    # Отправляем уведомление о прохождении первого тура
    try:
        await bot.send_message(
            chat_id=1736442606,
            text="🎉 <b>Поздравляем! Вы прошли первый тур!</b>\n\n"
                 "Напишите @marquezpht, чтобы выбрать время для созвона.",
            parse_mode="HTML"
        )
        print("Уведомление о прохождении первого тура отправлено!")
    except Exception as e:
        print(f"Ошибка при отправке уведомления: {e}")
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())