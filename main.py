import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from dotenv import load_dotenv

load_dotenv()

# ==================== НАСТРОЙКИ ====================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# ==================== ОБРАБОТЧИКИ ====================

@dp.message(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer(
        "🕵️‍♂️ <b>Sherlock Digital</b> — помощник цифрового поиска\n\n"
        "Я помогаю собирать информацию из открытых источников.\n"
        "Выбери действие или просто напиши запрос.",
        parse_mode="HTML"
    )

@dp.message()
async def universal_handler(message: types.Message):
    await message.answer(
        "🔍 Получил запрос. Сейчас анализирую...\n"
        "(Здесь будет подключаться ИИ и поисковые функции)"
    )

# ==================== WEBHOOK ====================

async def on_startup(bot: Bot):
    await bot.set_webhook(WEBHOOK_URL)
    print("✅ Webhook установлен")

async def on_shutdown(bot: Bot):
    await bot.delete_webhook()
    print("🛑 Webhook удалён")

def main():
    logging.basicConfig(level=logging.INFO)

    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    web.run_app(app, host="0.0.0.0", port=10000)

if __name__ == "__main__":
    main()
