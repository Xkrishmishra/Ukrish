import os
import re
import subprocess
import sys
import traceback
from inspect import getfullargspec
from io import StringIO
from time import time

from pyrogram import Client, filters
from pyrogram.types import Message

from config import OWNER_ID
from Vivek import app


async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {a}" for a in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


async def edit_or_reply(msg: Message, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    await func(**{k: v for k, v in kwargs.items() if k in spec})


@app.on_edited_message(
    filters.command(["eval", "ev"])
    & filters.user(OWNER_ID)
    & ~filters.forwarded
    & ~filters.via_bot,
    group=6,
)
@app.on_message(
    filters.command(["eval", "ev"])
    & filters.user(OWNER_ID)
    & ~filters.forwarded
    & ~filters.via_bot,
    group=6,
)
@app.bot.on_edited_message(
    filters.command(["eval", "ev"])
    & filters.user(OWNER_ID)
    & ~filters.forwarded
    & ~filters.via_bot,
    group=6,
)
@app.bot.on_message(
    filters.command(["eval", "ev"])
    & filters.user(OWNER_ID)
    & ~filters.forwarded
    & ~filters.via_bot,
    group=6,
)
async def executor(client: Client, message: Message):
    if len(message.command) < 2:
        return await edit_or_reply(message, text="<b>ᴡʜᴀᴛ ʏᴏᴜ ᴡᴀɴɴᴀ ᴇxᴇᴄᴜᴛᴇ ?</b>")
    try:
        cmd = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await message.delete()
    t1 = time()
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = "\n"
    if exc:
        evaluation += exc
    elif stderr:
        evaluation += stderr
    elif stdout:
        evaluation += stdout
    else:
        evaluation += "Success"
    final_output = f"<b>⥤ ʀᴇsᴜʟᴛ :</b>\n<pre language='python'>{evaluation}</pre>"
    if len(final_output) > 4096:
        filename = "output.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(evaluation))
        t2 = time()
        await message.reply_document(
            document=filename,
            caption=f"<b>⥤ ᴇᴠᴀʟ :</b>\n<code>{cmd[0:1000]}</code>\n\n<b>⥤ ʀᴇsᴜʟᴛ :</b>\nAttached Document",
            quote=False,
        )
        await message.delete()
        os.remove(filename)
    else:
        t2 = time()
        await edit_or_reply(message, text=final_output)


@app.on_edited_message(
    filters.command("sh")
    & filters.user(OWNER_ID)
    & ~filters.forwarded
    & ~filters.via_bot,
    group=6,
)
@app.on_message(
    filters.command("sh")
    & filters.user(OWNER_ID)
    & ~filters.forwarded
    & ~filters.via_bot,
    group=6,
)
@app.bot.on_edited_message(
    filters.command("sh")
    & filters.user(OWNER_ID)
    & ~filters.forwarded
    & ~filters.via_bot,
    group=6,
)
@app.bot.on_message(
    filters.command("sh")
    & filters.user(OWNER_ID)
    & ~filters.forwarded
    & ~filters.via_bot,
    group=6,
)
async def shellrunner(client: Client, message: Message):
    if len(message.command) < 2:
        return await edit_or_reply(message, text="<b>ᴇxᴀᴍᴩʟᴇ :</b>\n/sh git pull")
    text = message.text.split(None, 1)[1]
    if "\n" in text:
        code = text.split("\n")
        output = ""
        for x in code:
            shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", x)
            try:
                process = subprocess.Popen(
                    shell,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
            except Exception as err:
                await edit_or_reply(message, text=f"<b>ERROR :</b>\n<pre>{err}</pre>")
            output += f"<b>{code}</b>\n"
            output += process.stdout.read()[:-1].decode("utf-8")
            output += "\n"
    else:
        shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", text)
        for a in range(len(shell)):
            shell[a] = shell[a].replace('"', "")
        try:
            process = subprocess.Popen(
                shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except Exception as err:
            print(err)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(
                etype=exc_type,
                value=exc_obj,
                tb=exc_tb,
            )
            return await edit_or_reply(
                message, text=f"<b>ERROR :</b>\n<pre>{''.join(errors)}</pre>"
            )
        output = process.stdout.read()[:-1].decode("utf-8")
    if str(output) == "\n":
        output = None
    if output:
        if len(output) > 4096:
            with open("output.txt", "w+") as file:
                file.write(output)
            await client.send_document(
                message.chat.id,
                "output.txt",
                reply_to_message_id=message.id,
                caption="<code>Output</code>",
            )
            return os.remove("output.txt")
        await edit_or_reply(message, text=f"<b>OUTPUT :</b>\n<pre>{output}</pre>")
    else:
        await edit_or_reply(message, text="<b>OUTPUT :</b>\n<code>None</code>")
    await message.stop_propagation()
