import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
import yt_dlp

API_ID = 8040113
API_HASH = 3fd7b5718bc69a9da7d68c5707138c29
BOT_TOKEN = 8571933537:AAFA1BHEWeZn-8D-s4Kp9C17F0nhC7BUh9Q
SESSION = "BQB6rrEAGt5mC4mmSZT_98zDe8XDSG47S8IxIFyDs5ikGsVn8NI94z67UPu5ng7Nwln-u0ZRGXmEYP29J0PisLo1V789_Ama58iXvoHSJ7ryljp64JLYncbFFcnM-e91gz0RwyMT3BjIAI-fsEEuPEyj_xiQcxz8f-smz0LY7TzaoRkQWsuuzikH0onrY1y9MkEdiieYmwXWB9sF0tsrpq5s4wsc1XPfTiv5gJ3S8AiPHHAS2EMKsxVxUNSQ_FIUWhNxuf02UU4zU2S-vuL88iYfXX2cAT33iBrf5TdPH8WB386f3avGJLK3W-WktuBE4e9Yb0vFb5ldxZGAEpIsvNmGRXNspwAAAAHEt0BVAAOmn-jLjFPa59bj7FwK1xOyy2TT3VMUD2XKq6AjwRsqsesQFmfz6j9HRUaJl4ZOSzBNx2w08x8m-lKhrpfP4QgAAAAHEt0BVAA"

bot = Client("bot", api_id=8040113, api_hash=3fd7b5718bc69a9da7d68c5707138c29, bot_token=8571933537:AAFA1BHEWeZn-8D-s4Kp9C17F0nhC7BUh9Q)
assistant = Client(SESSION, api_id=8040113, api_hash=3fd7b5718bc69a9da7d68c5707138c29)

call = PyTgCalls(assistant)

def search_song(query):
    ydl_opts = {
        "format": "bestaudio",
        "outtmpl": "song.%(ext)s",
        "quiet": True,
        "noplaylist": True,
    }

    if not query.startswith("http"):
        query = f"ytsearch:{query}"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=True)
        if "entries" in info:
            info = info["entries"][0]

    return "song.webm", info["title"]

@bot.on_message(filters.command("play"))
async def play(_, message):
    if len(message.command) < 2:
        return await message.reply("Give song name or YouTube link")

    query = " ".join(message.command[1:])
    file, title = search_song(query)

    await assistant.join_chat(message.chat.id)

    await call.join_group_call(
        message.chat.id,
        AudioPiped(file)
    )

    await message.reply(f"▶️ Playing: {title}")

async def main():
    await bot.start()
    await assistant.start()
    await call.start()
    print("Bot running")
    await asyncio.Event().wait()

asyncio.run(main())
