import asyncio

from pyrogram import Client
from pyrogram import __version__ as v

API_ID = input("\nEnter Your API_ID:\n > ")
API_HASH = input("\nEnter Your API_HASH:\n > ")

i = Client(
    "Cute",
    in_memory=True,
    api_id=API_ID,
    api_hash=API_HASH,
    app_version=f"Cute {v}",
)


async def main():
    await i.start()
    ss = await i.export_session_string()
    print("\nHERE IS YOUR STRING SESSION, COPY IT, DON'T SHARE!!\n")
    print(f"\n{ss}\n")
    print("\n STRING GENERATED\n")
    xx = f"HERE IS YOUR STRING SESSION, COPY IT, DON'T SHARE!!\n\n`{ss}`\n\n STRING GENERATED"
    try:
        await i.send_message("me", xx)
    except BaseException:
        pass


asyncio.run(main())
