import requests
import yt_dlp
from pyrogram import Client, filters

API_ID = 8040113
API_HASH = "3fd7b5718bc69a9da7d68c5707138c29"
BOT_TOKEN = "8571933537:AAFA1BHEWeZn-8D-s4Kp9C17F0nhC7BUh9Q"
AUDD_API = "104c74cfda7e8fcc409024575232bab8"

bot = Client("song-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


# 🎧 Download audio from YouTube
def download_song(query):
    ydl_opts = {
        "format": "bestaudio",
        "outtmpl": "song.%(ext)s",
        "quiet": True,
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=True)
        if "entries" in info:
            info = info["entries"][0]

    return "song.webm", info["title"]


# 🔎 Recognize music
@bot.on_message(filters.audio | filters.voice | filters.video)
async def recognize(_, message):
    msg = await message.reply("🎧 Recognizing song...")

    file_path = await message.download()

    with open(file_path, "rb") as f:
        result = requests.post(
            "https://api.audd.io/",
            data={"api_token": AUDD_API, "return": "spotify"},
            files={"file": f},
        ).json()

    if result["status"] != "success" or not result["result"]:
        return await msg.edit("❌ Song not recognized")

    song = result["result"]
    title = song["title"]
    artist = song["artist"]

    await msg.edit(f"🎵 {title}\n👤 {artist}\n⬇️ Downloading...")

    # 🎶 Download song from YouTube
    file, yt_title = download_song(f"{title} {artist}")

    await message.reply_audio(
        file,
        title=title,
        performer=artist
    )

    await msg.delete()


bot.run()
