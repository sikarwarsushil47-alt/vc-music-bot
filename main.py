import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
import yt_dlp

API_ID = 8040113
API_HASH = 3fd7b5718bc69a9da7d68c5707138c29
BOT_TOKEN = 8571933537:AAFA1BHEWeZn-8D-s4Kp9C17F0nhC7BUh9Q
SESSION = "BQB6rrEATW2lWuovSRy285dd5H3hTVSMZco1TWRyhol1ak6KUOsGZz4LODcLVPoOJ2ykWp9EuC6RpDtxxcX4o3begjzEwSyTJu2ioCa03o3EG2XtFQn8ENbElJRZ0KmcdqTGroeiuJiluP7qq-4YU5HAq0_UT7QgxFkax_M7hsdlz9KBD2e-FHSTCq9aL0OgNrjqBrGRjN09ilEOgBZrzpWrNazRvzR7yTmL9WP-BJPKuXpEKDZ9rj2VAyLwbh3x9-GDGVi3ROmn-jLjFPa59bj7FwK1xOyy2TT3VMUD2XKq6AjwRsqsesQFmfz6j9HRUaJl4ZOSzBNx2w08x8m-lKhrpfP4QgAAAAHEt0BVAA"

bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
assistant = Client(SESSION, api_id=API_ID, api_hash=API_HASH)

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
