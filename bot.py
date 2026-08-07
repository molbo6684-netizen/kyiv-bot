import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart

# Отримуємо токен з змінних оточення Render
TOKEN = os.getenv("8655641728:AAH9pOJ8GgDwTsViVrgWh56LC5sOxbfFjzM")

if not TOKEN:
    raise ValueError("Не знайдено BOT_TOKEN у змінних середовища!")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Команда /start
@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(
        "Привіт! Бот для сповіщень успішно працює на сервері 24/7.\n\n"
        "Доступні команди:\n"
        "/status - перевірити стан бота\n"
        "/help - допомога"
    )

# Команда /status
@dp.message(Command(commands=["status"]))
async def status_cmd(message: types.Message):
    await message.answer("🟢 Бот в активному стані, з'єднання з Telegram встановлено.")

# Команда /help
@dp.message(Command(commands=["help"]))
async def help_cmd(message: types.Message):
    await message.answer("Сюди можна буде додати налаштування підписок на сповіщення чи інші функції.")

async def main():
    print("Бот запускається...")
    # Видаляємо вебхуки, які могли залишитися, і запускаємо опитування
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
