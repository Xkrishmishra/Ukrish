from pyrogram import filters
from pyrogram.errors import UsernameInvalid

from Vivek import app


@app.on_message(filters.sudo & filters.command(["common_chats"]))
async def get_common_chats(client, message):

    if len(message.command) < 2 and not message.reply_to_message:
        return await message.reply_text(
            "Usage: /common_chats @username or reply to a user."
        )

    if message.reply_to_message:
        username = (
            message.reply_to_message.from_user.username
            or message.reply_to_message.from_user.id
        )
    else:
        username = message.command[1]

    try:
        common_chats = await app.get_common_chats(username)
    except UsernameInvalid:
        return await message.reply_text(
            "The username is invalid. Please provide a valid username."
        )

    if not common_chats:
        return await message.reply_text("No common chats found.")

    msg = "Found Some Common Chats:\n\n"
    for chat in common_chats:
        title = chat.title or "Untitled Chat"
        chat_id = chat.id
        username = chat.username or "Private Group"
        members_count = chat.members_count or "Unknown"

        msg += f"**Chat Name:** {title}\n    ID: {chat_id}\n    Username: @{username}\n    Members: {members_count}\n\n"

    await message.reply_text(msg)
