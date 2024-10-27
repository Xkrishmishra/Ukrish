import re
from typing import List, Union

from pyrogram import Client, filters
from pyrogram.types import Message

from config import ONLY_FOR_SUDO, OWNER_ID, PREFIX

SPACE = True


def edit_filters():

    filters.reaction = filters.create(
        lambda _, __, m: bool(m.reactions), "ReactionFilter"
    )
    if ONLY_FOR_SUDO:
        filters.sudo = filters.create(
            lambda _, __, m: bool(
                m.from_user and (m.from_user.id in OWNER_ID or m.from_user.is_self)
            ),
            "SudoFilter",
        )
    else:

        filters.sudo = filters.create(
            lambda _, __, m: bool(
                m.from_user
                and (
                    m.from_user.id in OWNER_ID
                    or m.from_user.is_self
                    or m.chat
                    and m.chat.is_admin
                )
            ),
            "SudoFilter",
        )

    def command(commands: Union[str, List[str]], case_sensitive: bool = False):
        command_re = re.compile(r"([\"'])(.*?)(?<!\\)\1|(\S+)")

        async def func(flt, client: Client, message: Message):
            username = client.me.username or ""
            text = message.text or message.caption
            message.command = None

            if not text:
                return False

            if SPACE:
                # If SPACE is True, consider the entire text if no prefix matches
                for prefix in PREFIX:
                    if text.startswith(prefix):
                        text = text[len(prefix) :].lstrip()
                        break
                else:
                    text = text.lstrip()
            else:
                for prefix in PREFIX:
                    if text.startswith(prefix):
                        text = text[len(prefix) :].lstrip()
                        break
                else:
                    return False

            for cmd in flt.commands:
                if re.match(
                    f"^(?:{cmd}(?:@?{username})?)(?:\s|$)",
                    text,
                    flags=0 if flt.case_sensitive else re.IGNORECASE,
                ):
                    without_command = re.sub(
                        f"{cmd}(?:@?{username})?\s?",
                        "",
                        text,
                        count=1,
                        flags=0 if flt.case_sensitive else re.IGNORECASE,
                    )

                    message.command = [cmd] + [
                        re.sub(r"\\([\"'])", r"\1", m.group(2) or m.group(3) or "")
                        for m in command_re.finditer(without_command)
                    ]

                    return True

            return False

        commands = commands if isinstance(commands, list) else [commands]
        commands = {c if case_sensitive else c.lower() for c in commands}

        return filters.create(
            func, "CommandFilter", commands=commands, case_sensitive=case_sensitive
        )

    filters.command = command
