import asyncio
import logging
import sys

from src.bot.main import start_bot

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        print("Бот остановлен вручную.")