import asyncio
import os
import random
from functools import wraps
from typing import Optional, Union

import httpx
from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, MessageEntityType
from pyrogram.types import Message
from youtubesearchpython.__future__ import VideosSearch

from config import LOG_GROUP_ID

S12KK = {}
pause = {}
mute = {}
active = []
chatlist = []


class MelodyError(Exception):

    def __init__(self, message):
        super().__init__(message)


class DownloadError(Exception):

    def __init__(self, errr: str):
        super().__init__(errr)


def S12K(chat_id: Optional[int] = None):
    if chat_id is not None:
        S12KK[1234] = chat_id
    return S12KK.get(1234) or LOG_GROUP_ID


class Vivek:

    @staticmethod
    async def get_url(message_1: Message) -> Union[str, None]:
        messages = [message_1]
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)

        text = ""
        offset = None
        length = None

        for message in messages:
            if offset:
                break
            if message.entities:
                for entity in message.entities:
                    if entity.type == MessageEntityType.URL:
                        text = message.text or message.caption
                        offset, length = entity.offset, entity.length
                        break
            elif message.caption_entities:
                for entity in message.caption_entities:
                    if entity.type == MessageEntityType.TEXT_LINK:
                        return entity.url

        if offset is None:
            return None

        return text[offset : offset + length]

    @staticmethod
    async def track(link: str, randomize=False):
        if "&" in link:
            link = link.split("&")[0]

        limit = 10 if randomize else 1
        results = VideosSearch(link, limit=limit)
        result_data = await results.next()

        if not result_data["result"]:
            raise MelodyError("No results Found in Search")

        if randomize:
            index = random.randint(3, 9)
            result = result_data["result"][index]
        else:
            result = result_data["result"][0]

        title = result["title"]
        duration_min = result["duration"]
        vidid = result["id"]
        yturl = result["link"]
        thumbnail = result["thumbnails"][0]["url"].split("?")[0]

        track_details = {
            "title": title,
            "link": yturl,
            "vidid": vidid,
            "duration_min": duration_min,
            "thumb": thumbnail,
        }
        return track_details

    @staticmethod
    async def run_shell_cmd(command):
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await process.communicate()
        return process.returncode, stdout.decode(), stderr.decode()

    @staticmethod
    async def download(vidid: str, video: bool = False):
        API = "https://api.cobalt.tools/api/json"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        }

        if video:
            path = os.path.join("downloads", f"{vidid}.mp4")
            data = {
                "url": f"https://www.youtube.com/watch?v={vidid}",
                "vQuality": "480",
            }
        else:
            path = os.path.join("downloads", f"{vidid}.m4a")
            data = {
                "url": f"https://www.youtube.com/watch?v={vidid}",
                "isAudioOnly": "True",
                "aFormat": "opus",
            }

        try:
            async with httpx.AsyncClient(http2=True) as client:
                response = await client.post(API, headers=headers, json=data)
                response.raise_for_status()

                results = response.json().get("url")
                if not results:
                    raise ValueError("No download URL found in the response")

                cmd = f'yt-dlp "{results}" -o "{path}"'
                returncode, stdout, stderr = await Vivek.run_shell_cmd(cmd)

                if returncode == 0 and os.path.isfile(path):
                    return path
                else:
                    raise DownloadError("Download failed or file not found.")

        except (
            httpx.RequestError,
            httpx.HTTPStatusError,
            ValueError,
            DownloadError,
        ) as e:
            raise DownloadError(f"Download failed after fallback attempt: {str(e)}")

    @staticmethod
    async def is_music_playing(chat_id: int) -> bool:
        return pause.get(chat_id, False)

    @staticmethod
    async def music_on(chat_id: int):
        pause[chat_id] = True

    @staticmethod
    async def music_off(chat_id: int):
        pause[chat_id] = False

    @staticmethod
    async def is_muted(chat_id: int) -> bool:
        return mute.get(chat_id, False)

    @staticmethod
    async def mute_on(chat_id: int):
        mute[chat_id] = True

    @staticmethod
    async def mute_off(chat_id: int):
        mute[chat_id] = False

    @staticmethod
    async def get_active_chats() -> list:
        return active

    @staticmethod
    async def is_active_chat(chat_id: int) -> bool:
        return chat_id in active

    @staticmethod
    async def add_active_chat(chat_id: int):
        if chat_id not in active:
            active.append(chat_id)

    @staticmethod
    async def remove_active_chat(chat_id: int):
        if chat_id in active:
            active.remove(chat_id)

    async def extract_userid(message, text: str):
        """
        NOT TO BE USED OUTSIDE THIS FILE
        """

        def is_int(text: str):
            try:
                int(text)
            except ValueError:
                return False
            return True

        text = text.strip()

        if is_int(text):
            return int(text)

        entities = message.entities
        app = message._client
        if len(entities) < 2:
            return (await app.get_users(text)).id
        entity = entities[1]
        if entity.type == MessageEntityType.MENTION:
            return (await app.get_users(text)).id
        if entity.type == MessageEntityType.TEXT_MENTION:
            return entity.user.id
        return None

    async def extract_user_and_reason(message, sender_chat=False):
        args = message.text.strip().split()
        text = message.text
        user = None
        reason = None

        try:
            if message.reply_to_message:
                reply = message.reply_to_message
                # if reply to a message and no reason is given
                if not reply.from_user:
                    if (
                        reply.sender_chat
                        and reply.sender_chat != message.chat.id
                        and sender_chat
                    ):
                        id_ = reply.sender_chat.id
                    else:
                        return None, None
                else:
                    id_ = reply.from_user.id

                if len(args) < 2:
                    reason = None
                else:
                    reason = text.split(None, 1)[1]
                return id_, reason

            # if not reply to a message and no reason is given
            if len(args) == 2:
                user = text.split(None, 1)[1]
                return await extract_userid(message, user), None

            # if reason is given
            if len(args) > 2:
                user, reason = text.split(None, 2)[1:]
                return await extract_userid(message, user), reason

            return user, reason

        except errors.UsernameInvalid:
            return "", ""

    async def extract_user(message):
        return (await extract_user_and_reason(message))[0]


async def has_permissions(
    client: Client, message: Message, permissions: Union[list, str, None] = None
) -> bool:
    """Check if the user and bot have the required permissions, and reply directly if not."""
    user = await client.get_chat_member(message.chat.id, message.from_user.id)

    if user.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
        return await message.reply_text("You are not an admin.")

    if permissions:
        if isinstance(permissions, str):
            permissions = [permissions]

        for permission in permissions:
            if not getattr(user.privileges, permission, False):
                return await message.reply_text(
                    f"You are missing the required permission: {permission}"
                )

    bot = await client.get_chat_member(message.chat.id, "self")

    if bot.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
        return await message.reply_text("The bot is not an admin.")

    if permissions:
        for permission in permissions:
            if not getattr(bot.privileges, permission, False):
                return await message.reply_text(
                    f"The bot is missing the required permission: {permission}"
                )

    return True


def adminsOnly(permissions: Union[list, str, None] = None):
    """Decorator to restrict access to commands based on user and bot permissions."""

    def decorator(func):
        @wraps(func)
        async def wrapper(client: Client, message: Message, *args, **kwargs):
            if await has_permissions(client, message, permissions):
                return await func(client, message, *args, **kwargs)

        return wrapper

    return decorator
