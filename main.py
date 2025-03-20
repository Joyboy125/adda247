from pyrogram import Client, idle
import logging
import asyncio
import subprocess

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


# Main function
async def main():
    await animebot.start()
    print("Bots are running...")
    await idle()
    await animebot.stop()
    print("Bot stopped.")

# Run the bot
if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(main())
