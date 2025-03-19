from pyrogram import Client, idle
import logging
import asyncio
import subprocess
from flask import Flask, request

# Check if FFmpeg is installed
try:
    subprocess.run(["ffmpeg", "-version"], check=True)
    print("✅ FFmpeg is installed and working!")
except FileNotFoundError:
    print("❌ FFmpeg is missing!")

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# API credentials
api_id = 20375588
api_hash = "1dad937cc8c9b35db882ebed1a064cfc"
bot_token = "6647141297:AAEW3aur3IJCsiRh2Wk0n6DcqUCZnmYSfgk"  # animemonster_bot

# Load plugins
plugins = {"root": "plugins"}

# Initialize bot
animebot = Client(name="animemonster_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token, plugins=plugins, sleep_threshold=15)

# Flask setup
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json()
    # Process the update
    return "OK"

# Function to run Flask in the background
async def run_flask():
    loop = asyncio.get_running_loop()
    from threading import Thread
    def start_flask():
        app.run(host="0.0.0.0", port=8080)
    Thread(target=start_flask, daemon=True).start()

# Main function
async def main():
    await run_flask()  # Start Flask in a separate thread
    await animebot.start()
    print("Bots are running...")
    await idle()
    await animebot.stop()
    print("Bot stopped.")

# Run the bot
if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(main())
    # asyncio.run(main())
