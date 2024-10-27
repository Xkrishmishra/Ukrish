from pyrogram import filters

from Vivek import app
from Vivek.utils.functions import chatlist


@app.on_message(filters.sudo & filters.command("playendless"))
async def endless(c, m):
    chat_id = m.chat.id
    if "on" in m.text.lower():
        if chat_id not in chatlist:
            chatlist.append(chat_id)
            await m.reply("Endless playback mode is now **ON**.")
        else:
            await m.reply("Endless playback mode is already **ON**.")
    elif "off" in m.text.lower():
        if chat_id in chatlist:
            chatlist.remove(chat_id)
            await m.reply("Endless playback mode is now **OFF**.")
        else:
            await m.reply("Endless playback mode was not **ON**.")
    else:
        await m.reply(
            "Usage: `!playendless on` to enable or `!playendless off` to disable."
        )
