import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.dispatcher.webhook import get_new_configured_app
from aiohttp import web
from aiohttp.web import Application
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] : #%(levelname)-8s - %(filename)s:%(lineno)d - %(name)s - %(message)s",
)


async def register_all_handlers(dp: Dispatcher) -> None:
    await register_start(dp)
    await register_google(dp)
    await register_yandex(dp)


async def on_startup(app: Application) -> None:
    bot_info = await bot.get_me()
    logging.info(f"🤙 Hello from {bot_info.full_name} [@{bot_info.username}]!")

    # Setting webhook URL
    await bot.set_webhook(url=config.WEBHOOK_URL)
    logging.info(f"Webhook was set on '{config.WEBHOOK_URL}'")

    await register_all_handlers(dp)


async def on_shutdown(app: Application) -> None:
    # Disconecting redis storage
    await dp.storage.close()
    await dp.storage.wait_closed()


# Initialize storage
storage = RedisStorage2(
    host=config.REDIS_STORAGE_HOST,
    port=config.REDIS_STORAGE_PORT,
    db=config.REDIS_STORAGE_DB,
    prefix="search_bot",
)


# Initialize bot and dispatcher
bot = Bot(token=config.API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)

# Initializing async task scheduler
bot_scheduler = AsyncIOScheduler(timezone="Europe/Moscow")


if __name__ == "__main__":
    from handlers.search_google import register_google
    from handlers.search_yandex import register_yandex
    from handlers.start import register_start

    bot_app = get_new_configured_app(dispatcher=dp, path=config.WEBHOOK_PATH)
    bot_app.on_startup.append(on_startup)
    bot_app.on_shutdown.append(on_shutdown)

    web.run_app(
        app=bot_app,
        host=config.WEBAPP_HOST,
        port=config.WEBAPP_PORT,
    )
