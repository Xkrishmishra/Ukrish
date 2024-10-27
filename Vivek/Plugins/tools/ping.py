from pyrogram import filters

from Vivek import app


@app.on_message(filters.command(["ping"]) & filters.sudo)
async def ping(client, message):
    await message.reply_text("I Am alive brooo")
