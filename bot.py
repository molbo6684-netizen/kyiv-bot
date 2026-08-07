import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

# Токен береться з налаштувань Render
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Привіт! Бот успішно запущений і працює!")

async def main():
    print("Бот запускається...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
