import os

from pyrogram import filters

from Vivek import app


@app.on_message(filters.command(["update", "up", "gitpull"]) & filters.sudo)
async def update_(client, message):
    await message.reply_text("Updating...")
    os.system("git pull && bash start")
