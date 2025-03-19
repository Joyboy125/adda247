from pyrogram import Client, idle 
import logging
import asyncio
import os
from pyrogram import Client, filters
from pyrogram.types import Message

import subprocess

try:
    subprocess.run(["ffmpeg", "-version"], check=True)
    print("✅ FFmpeg is installed and working!")
except FileNotFoundError:
    print("❌ FFmpeg is missing!")


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


api_id = 20375588
api_hash = "1dad937cc8c9b35db882ebed1a064cfc"

animemonster_bot = "6647141297:AAEW3aur3IJCsiRh2Wk0n6DcqUCZnmYSfgk"
Joyboy2_bot = "6432721045:AAF9oIqBCHPbJk0aJJsSeGCO4aF3qKmvq-w"
manhwa_robot = "7100114766:AAEqBIquT_6C-uSggMIWFoOuOQROjx-2fTI"


plugins={"root": "plugins"}

animebot = Client(name="animemonster_bot", api_id=api_id, api_hash=api_hash, bot_token=animemonster_bot, plugins=plugins, sleep_threshold=15)

from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json()
    # Process the update
    return "OK"


async def main():
    try:
        await animebot.start()
        print("Bots are running...")
        await idle()
    except (ApiIdInvalid, ApiIdPublishedFlood):
        raise Exception("Your API_ID/API_HASH is not valid.")
    except AccessTokenInvalid:
        raise Exception("Your BOT_TOKEN is not valid.")
    finally:
        await animebot.stop()
        print("Bot stopped.")

if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    app.run(host="0.0.0.0", port=8080)
    loop.run_until_complete(main())
    print("Bot stopped.")
