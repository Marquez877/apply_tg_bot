import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
import os
from aiogram.utils.keyboard import InlineKeyboardBuilder

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise ValueError("API_TOKEN is not set in the environment variables.")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
@dp.message(Command("start"))
async def start_command(message: types.Message):
    
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Main menu", callback_data="main_menu"))
    await message.answer("Hello! I'm your bot. How can I assist you today?", reply_markup=builder.as_markup())

@dp.message(Command("help"))
async def help_command(message: types.Message):

    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Back to Menu", callback_data="back_to_menu"))
    await message.answer("Here are the commands you can use:\n/start - Start the bot\n/help - Get help information", reply_markup=builder.as_markup())

@dp.message(Command("application"))
async def application_command(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Apply Now", url="https://example.com/application"))
    builder.add(types.InlineKeyboardButton(text="Back to Menu", callback_data="back_to_menu"))
    await message.answer("To apply, please fill out the application form at: https://example.com/application", reply_markup=builder.as_markup())








# Обработчик callback_query для "main_menu"
async def main_menu_callback(callback_query: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Help", callback_data="help"))
    builder.add(types.InlineKeyboardButton(text="Application", callback_data="application"))
    await callback_query.message.edit_text(text= f'''Hello! Welcome to the bot.'''
    ''' Create an inline keyboard with a button to go to the main menu'''
    '''You can use the following commands:''', reply_markup=builder.as_markup())
    await callback_query.answer()

async def help_callback(callback_query: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Back to Menu", callback_data="back_to_menu"))
    await callback_query.message.edit_text(
        "Here are the commands you can use:\n/start - Start the bot\n/help - Get help information",
        reply_markup=builder.as_markup()
    )
    await callback_query.answer()
# Регистрация обработчика с фильтром по callback_data == "main_menu"

async def back_to_menu_callback(callback_query: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Main Menu", callback_data="main_menu"))
    await callback_query.message.edit_text("You are back to the main menu.", reply_markup=builder.as_markup())
    await callback_query.answer()

async def application_callback(callback_query: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Apply Now", url="https://example.com/application"))
    builder.add(types.InlineKeyboardButton(text="Back to Menu", callback_data="back_to_menu"))
    await callback_query.message.edit_text("To apply, please fill out the application form at: https://example.com/application", reply_markup=builder.as_markup())
    await callback_query.answer()








dp.callback_query.register(main_menu_callback, lambda c: c.data == "main_menu")
dp.callback_query.register(help_callback, lambda c: c.data == "help")
dp.callback_query.register(back_to_menu_callback, lambda c: c.data == "back_to_menu")
dp.callback_query.register(application_callback, lambda c: c.data == "application")








async def main():
    print("Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
