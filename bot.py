import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("Не знайдено BOT_TOKEN у змінних середовища!")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Використовуємо 1 основний топ-канал, щоб не було дублювання інформації
SOURCE_CHAT_IDS = [
    "@war_monitor",  # Головний детальний моніторинг цілей
]

TARGET_GROUP_ID = -1004335784419  # <--- Впишіть сюди ID вашої групи (з мінусом на початку)

# Зберігаємо останнє повідомлення, щоб уникнути спаму та повторів
last_sent_message = ""

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Бот авто-моніторингу запрацював без дублів! 🛡")

@dp.message()
async def auto_forward_alert(message: types.Message):
    global last_sent_message
    
    chat_identifier = f"@{message.chat.username}" if message.chat.username else message.chat.id
    
    if chat_identifier in SOURCE_CHAT_IDS or message.chat.id in SOURCE_CHAT_IDS:
        if message.text:
            # Захист від повторення однакових повідомлень підряд
            if message.text == last_sent_message:
                return  # Пропускаємо, якщо таке повідомлення щойно було
            
            keywords = ["бпла", "ракета", "курс", "летить", "вибух", "тривога", "хід", "ціль", "київ"]
            text_lower = message.text.lower()
            
            if any(word in text_lower for word in keywords):
                last_sent_message = message.text   запам'ятовуємо текст
                
                alert_message = f"🚨 **ОПЕРАТИВНИЙ МОНІТОРИНГ** 🚨\n\n{message.text}"
                try:
                    await bot.send_message(chat_id=TARGET_GROUP_ID, text=alert_message, parse_mode="Markdown")
                except Exception as e:
                    print(f"Помилка відправки в групу: {e}")

async def main():
    print("Бот запускається...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
