import os
import requests
import yt_dlp
from pyrogram import Client, filters

API_ID = 8040113          
API_HASH = "3fd7b5718bc69a9da7d68c5707138c29"   
BOT_TOKEN = "8571933537:AAFA1BHEWeZn-8D-s4Kp9C17F0nhC7BUh9Q" 
AUDD_KEY = "104c74cfda7e8fcc409024575232bab8" 

app = Client("bot", api_id=8040113, api_hash=3fd7b5718bc69a9da7d68c5707138c29, bot_token=8571933537:AAFA1BHEWeZn-8D-s4Kp9C17F0nhC7BUh9Q)


# ===============================
# 🎧 AUDIO RECOGNITION
# ===============================
@app.on_message(filters.audio | filters.voice | filters.video)
async def recognize(client, message):

    file = await message.download()

    with open(file, "rb") as f:
        r = requests.post(
            "https://api.audd.io/",
            data={"api_token": AUDD_KEY, "return": "apple_music,spotify"},
            files={"file": f}
        )

    result = r.json()

    if result["result"]:
        title = result["result"]["title"]
        artist = result["result"]["artist"]

        await message.reply(
            f"🎵 **{title} — {artist}**\n\nSend song name to download 🎧"
        )
    else:
        await message.reply("❌ Song not recognized")


# ===============================
# 🎵 TEXT → DOWNLOAD SONG
# ===============================
@app.on_message(filters.text & ~filters.command("start"))
async def download_song(client, message):

    query = message.text

    await message.reply("🔎 Searching song...")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "song.%(ext)s",
        "quiet": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=True)
        entry = info["entries"][0]
        filename = ydl.prepare_filename(entry)

    await message.reply_audio(filename, title=entry["title"])

    os.remove(filename)


# ===============================
# START COMMAND
# ===============================
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply(
        "🎧 Send audio to identify\n"
        "🎵 Send song name to download"
    )


app.run()
