import os
import requests
from pyrogram import Client, filters
from pyrogram.types import Message
import ffmpeg
import asyncio

"""sudo apt update && sudo apt install ffmpeg -y
"""

def download_ts_file(url, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
    else:
        print(f"Failed to download {url}")


def download_all_ts_files(BASE_URL, End_segment, OUTPUT_DIR):
    ts_files = []
    for i in range(0, End_segment + 1):  # Adjust the range based on the number of .ts files
        ts_url = f"{BASE_URL}{i}.ts"  # Adjust the URL pattern as needed
        ts_file = os.path.join(OUTPUT_DIR, f"segment_{i}.ts")
        download_ts_file(ts_url, ts_file)
        ts_files.append(ts_file)
    return ts_files

def create_concat_file(OUTPUT_DIR):
    """Create a properly formatted file_list.txt inside ts_files."""
    concat_file = os.path.join(OUTPUT_DIR, "file_list.txt")

    with open(concat_file, "w") as f:
        for ts_file in sorted(os.listdir(OUTPUT_DIR)):  # Ensure order
            if ts_file.endswith(".ts"):
                f.write(f"file '{ts_file}'\n")  # Correct relative path

    return concat_file

def merge_ts_files(OUTPUT_DIR, OUTPUT_VIDEO):
    concat_file = create_concat_file(OUTPUT_DIR)
    print("Merging video segments...")
    try:
        (
        ffmpeg.input(concat_file, f="concat", safe=0).output(OUTPUT_VIDEO, c="copy").run()
        )
        print(f"✅ Merged video saved as {OUTPUT_VIDEO}")

    except Exception as e:
        print(f"❌ Error during merging: {e}")
    print(f"✅ Video merged as {OUTPUT_VIDEO}")


def compress_video(input_file, output_file):

    """ Compress the video using ffmpeg """
    crf=28
    preset="fast"
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found!")
        return

    process = (
    ffmpeg.input(input_file)
    .output(output_file, vcodec="libx264", crf=23, preset="fast", acodec="aac", **{"b:a": "128k"})
    .global_args("-progress", "pipe:1", "-nostats")  # ✅ Enables progress output
    .run_async(pipe_stdout=True, pipe_stderr=True))

    while True:
        line = process.stdout.readline().decode("utf-8", errors="ignore")
        if not line:
            break
        if "out_time_ms" in line:  # 🔹 Extracts progress in microseconds
            time_ms = int(line.split("=")[1])
            time_sec = time_ms / 1_000_000
            print(f"🔄 Encoding Progress: {time_sec:.2f} sec", end="\r", flush=True)

    process.wait()
    print("\n✅ Compression complete!")

"https://vidz.adda247.com/ivs/v1/748804974185/EXTuk2ShEQ7I/2024/12/13/8/34/d2bZ8lKV8E8e/media/hls/720p30/109.ts"

@Client.on_message(filters.command("download_video"))
async def Download_video(client: Client, message: Message):

    
    try:
        if len(message.command) == 1:
            return await message.reply_text("Give the video url")

        # Extract the format from the command
        BASE_URL = message.text.split("/download_video", 1)[1].strip()

        try:
            first_message = await client.ask(
                    text="Send me total segment numbers",
                    chat_id=message.chat.id,
                    filters=(filters.text),
                    timeout=50 
            )
        except asyncio.TimeoutError:
                await message.reply_text("Request timed out. Please try again.")
                return
        
        me = await client.get_me()
        bot_username = me.username

        OUTPUT_DIR = f"{bot_username}_ts_files"  
        OUTPUT_VIDEO = f"{bot_username}_output.mp4" 
        COMPRESSED_VIDEO = f"{bot_username}_compressed.mp4"
        
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        await message.reply_text("Starting video download and processing...")

        ts_files = download_all_ts_files(BASE_URL, int(first_message.text), OUTPUT_DIR)
        await message.reply_text("All .ts files downloaded. merging the video....")

        # Step 2: Merge .ts files
        merge_ts_files(OUTPUT_DIR, OUTPUT_VIDEO)
        await message.reply_text("Video merged. compressing video....")

        # Step 3: Compress the video
        compress_video(OUTPUT_VIDEO, COMPRESSED_VIDEO)
        await message.reply_text("Video compressed.")

        # Step 4: Upload the video to Telegram
        await message.reply_video(COMPRESSED_VIDEO, caption="Here's your compressed video!")

        if os.path.exists(OUTPUT_DIR):
            for ts_file in ts_files:
                os.remove(ts_file)
        if os.path.exists(f"{OUTPUT_DIR}/file_list.txt"):
            os.remove(f"{OUTPUT_DIR}/file_list.txt")
        if os.path.exists(OUTPUT_VIDEO):
            os.remove(OUTPUT_VIDEO)
        if os.path.exists(COMPRESSED_VIDEO):
            os.remove(COMPRESSED_VIDEO)

    except Exception as e:
        await message.reply(f" Got error in this command : {e}")


@Client.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    await message.reply(f"i am online")