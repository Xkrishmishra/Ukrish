import asyncio
import importlib

from pyrogram import idle

from config import LOG_GROUP_ID
from Vivek import HELPABLE, LOGGER, app, call
from Vivek.plugins import ALL_MODULES


async def main():
    LOGGER("Vivek").info("Staring Clients")

    await app.start()
    await app.bot.start()
    await app.bot.send_message(LOG_GROUP_ID, "started")
    for all_module in ALL_MODULES:
        imported_module = importlib.import_module("Vivek.plugins" + all_module)
        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
                HELPABLE[imported_module.__MODULE__.lower()] = imported_module
    await call.start()
    LOGGER("Vivek").info("Clients Started Successfully")
    await idle()

    await app.stop()
    await app.bot.stop()


if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(main())
