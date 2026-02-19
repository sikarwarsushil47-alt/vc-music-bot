import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
import yt_dlp

API_ID = int("8040113")
API_HASH = "3fd7b5718bc69a9da7d68c5707138c29"
BOT_TOKEN = "8571933537:AAFA1BHEWeZn-8D-s4Kp9C17F0nhC7BUh9Q"
SESSION = "assistant"

bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
assistant = Client(SESSION, api_id=API_ID, api_hash=API_HASH)

call = PyTgCalls(assistant)

def search_or_download(query):
    ydl_opts = {
        "format": "bestaudio",
        "outtmpl": "song.%(ext)s",
        "quiet": True,
        "noplaylist": True,
    }

    # If not a link → search YouTube
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
    file, title = search_or_download(query)

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
    print("Smart VC Bot Running")
    await asyncio.Event().wait()

asyncio.run(main())
