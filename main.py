from pyrogram import Client, idle 
import logging
import asyncio
import os
from pyrogram import Client, filters
from pyrogram.types import Message


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

Joyboy2bot = Client(name="Joyboy2_bot", api_id=api_id, api_hash=api_hash, bot_token=Joyboy2_bot, plugins=plugins, sleep_threshold=15)

manhwabot = Client(name="manhwa_robot", api_id=api_id, api_hash=api_hash, bot_token=manhwa_robot, plugins=plugins, sleep_threshold=15)

async def main():
    try:
        await animebot.start()
        await Joyboy2bot.start()
        await manhwabot.start()
        print("Bots are running...")
        await idle()
    except (ApiIdInvalid, ApiIdPublishedFlood):
        raise Exception("Your API_ID/API_HASH is not valid.")
    except AccessTokenInvalid:
        raise Exception("Your BOT_TOKEN is not valid.")
    finally:
        await animebot.stop()
        await Joyboy2bot.stop()
        await manhwabot.stop()
        print("Bot stopped.")

if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(main())
    print("Bot stopped.")


# class animemonster(Client):
#     def __init__(self):
#         super().__init__(
#             name="animemonster_bot",
#             api_id=api_id,
#             api_hash=api_hash,
#             bot_token=animemonster_bot,
#             workers=200,
#             plugins={"root": "plugins"},
#             sleep_threshold=15,
#         )

# class Joyboy2(Client):
#     def __init__(self):
#         super().__init__(
#             name="Joyboy2_bot",
#             api_id=api_id,
#             api_hash=api_hash,
#             bot_token=Joyboy2_bot,
#             workers=200,
#             plugins={"root": "plugins"},
#             sleep_threshold=15,
#         )

# class manhwa(Client):
#     def __init__(self):
#         super().__init__(
#             name="manhwa_robot",
#             api_id=api_id,
#             api_hash=api_hash,
#             bot_token=manhwa_robot,
#             workers=200,
#             plugins={"root": "plugins"},
#             sleep_threshold=15,
#         )


# async def main():

#     bot1 = animemonster()
#     bot2 = Joyboy2()
#     bot3 = manhwa()

#     await asyncio.gather(bot1.start(), bot2.start(), bot3.start())
#     print("Both bots are running...")

#     await asyncio.Event().wait()

# if __name__ == "__main__":
#     asyncio.run(main())