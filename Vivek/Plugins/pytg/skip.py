from pyrogram import filters

from Vivek import MusicPlayer as call
from Vivek import app
from Vivek.utils.functions import Vivek


@app.on_message(filters.sudo & filters.command("skip"))
async def skip_(client, message):
    if not await Vivek.is_active_chat(message.chat.id):
        return await message.reply_text("I am not streaming On VoiceChat")
    await call.change_stream(message.chat.id)
