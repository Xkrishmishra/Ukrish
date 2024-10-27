from pyrogram import filters
from pyrogram.types import CallbackQuery

from Vivek import app


@app.bot.on_callback_query(filters.regex("close"))
async def close_menu(_, query: CallbackQuery):
    try:
        await query.answer()
        await query.message.delete()
    except:
        pass
