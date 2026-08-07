import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("Не знайдено BOT_TOKEN у змінних середовища!")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Список ID або username каналів/груп, звідки потрібно брати інформацію (можна додавати скільки завгодно через кому)
SOURCE_CHAT_IDS = [
    "@kyiv_info_live_radar",  # Приклад першого джерела
    "@kyivskyi_kupol",        # Приклад другого джерела
    # -100111111111           # Можна додавати і через числовий ID якщо це закрита група
]

# ID вашої групи, куди бот повинен автоматично надсилати сповіщення
TARGET_GROUP_ID = -1001234567890  # Замініть на ID вашої цільової групи

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Бот для авто-моніторингу тривог з кількох джерел запущено! 🛡")

# Автоматичний перехоплювач повідомлень
@dp.message()
async def auto_forward_alert(message: types.Message):
    # Визначаємо ідентифікатор поточного чату (або юзернейм з @, або числовий ID)
    chat_identifier = f"@{message.chat.username}" if message.chat.username else message.chat.id
    
    # Перевіряємо, чи є чат у нашому списку джерел
    if chat_identifier in SOURCE_CHAT_IDS or message.chat.id in SOURCE_CHAT_IDS:
        if message.text:
            # Фільтруємо за ключовими словами, щоб не пересилати зайве
            keywords = ["бпла", "ракета", "курс", "летить", "вибух", "тривога", "хід", "ціль"]
            text_lower = message.text.lower()
            
            if any(word in text_lower for word in keywords):
                alert_message = f"🚨 **ОПЕРАТИВНИЙ МОНІТОРИНГ** 🚨\n\n{message.text}"
                try:
                    await bot.send_message(chat_id=TARGET_GROUP_ID, text=alert_message, parse_mode="Markdown")
                except Exception as e:
                    print(f"Помилка відправки в цільову групу: {e}")

async def main():
    print("Бот запускається...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
