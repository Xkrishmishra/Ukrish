import re

from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message

from Vivek import MusicPlayer as call
from Vivek import app
from Vivek.utils.functions import DownloadError, MelodyError, Vivek
from Vivek.utils.queue import Queue


@app.on_message(filters.command(["play", "vplay"]) & filters.sudo)
async def play_command(client, message: Message):
    mystic = await message.reply_text("Processing....")
    user_id = message.from_user.id
    user_name = message.from_user.mention

    url = await Vivek.get_url(message)
    query = None
    if url:
        match = re.search(
            r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=|embed\/|v\/|live_stream\?stream_id=|(?:\/|\?|&)v=)?([^&\n]+)",
            url,
        )
        if match:
            if "playlist" in url:
                return await mystic.edit("Youtube Playlist Url not supported for now")
            if "shorts" in url:
                match = re.search(
                    r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=|embed\/|v\/|shorts\/|live_stream\?stream_id=|(?:\/|\?|&)v=)?([^&\n?#]+)",
                    url,
                )

                if match:
                    videoid = match.group(1)

                    query = f"https://www.youtube.com/watch?v={videoid}"
                else:
                    return await mystic.edit(
                        "look like you want to play a YotuTube Shorts by i can play only Video or Songs"
                    )
            elif "https://youtu.be" in url:
                videoid = url.split("/")[-1].split("?")[0]
                query = f"https://www.youtube.com/watch?v={videoid}"
            else:
                videoid = match.group(1)
                query = f"https://www.youtube.com/watch?v={videoid}"
        else:
            return await mystic.edit("Provide a name or YouTube url")
    else:
        if len(message.command) < 2:
            return await mystic.edit("What do you want to play baby")
        query = message.text.split(None, 1)[1]

    details = await Vivek.track(query)
    title = details["title"]
    url = details["link"]
    duration_min = details["duration_min"]
    vidid = details["vidid"]
    video = message.command[0][0] == "v"

    try:
        file_path = await Vivek.download(vidid, video=video)
    except DownloadError as e:
        return await mystic.edit(e)
    except Exception as e:
        return await mystic.edit(e)

    if await Vivek.is_active_chat(message.chat.id):
        await Queue.add(
            message.chat.id,
            chatid=message.chat.id,
            title=title,
            duration=duration_min,
            vidid=vidid,
            video=video,
            file_path=file_path,
            by=user_name,
        )
        count = len(await Queue.get_queues(message.chat.id)) - 1
        return await mystic.edit_text(
            f"<b>Added To Queue At {count}</b>\n<b>Title:</b> {title}\n<b>Duration</b>: {duration_min}\n<b>By</b>: {user_name}",
            disable_web_page_preview=True,
            parse_mode=ParseMode.HTML,
        )

    try:
        await call.play(message.chat.id, file_path, video)
    except MelodyError as e:
        return await mystic.edit(e)
    except Exception as e:
        return await mystic.edit(e)
    await Queue.add(
        message.chat.id,
        chatid=message.chat.id,
        title=title,
        duration=duration_min,
        vidid=vidid,
        video=video,
        file_path=file_path,
        by=user_name,
    )

    await Vivek.add_active_chat(message.chat.id)
    await app.send_message(
        message.chat.id,
        f"**Started Streaming**\n\n**Title**: {title}\n**Duration**: {duration_min}\n**by** {user_name}",
        disable_web_page_preview=True,
    )

    await mystic.delete()
