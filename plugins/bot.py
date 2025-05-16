import os
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, InputMediaPhoto, CallbackQuery, InputMediaVideo

import ffmpeg
import asyncio
import logging

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

import os
import subprocess

def ts_to_image(ts_file, output_image="output.jpg", time="00:00:01"):
    """
    Extracts a frame from a TS segment and saves it as an image.

    :param ts_file: Path to the .ts video file
    :param output_image: Path to save the extracted image (default: output.jpg)
    :param time: Timestamp (HH:MM:SS) to capture the frame (default: 1 second)
    :return: Path of the saved image
    """
    command = [
        "ffmpeg",
        "-i", ts_file,        # Input file
        "-ss", time,          # Time position
        "-vframes", "1",      # Capture a single frame
        output_image,         # Output file
        "-y"                  # Overwrite if file exists
    ]
    
    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Image saved as {output_image}")
        return output_image
    except subprocess.CalledProcessError as e:
        print(f"Error extracting image: {e}")
        return None

# Example usage


def natural_sort_key(s):
    """Extract numbers from filename for proper sorting."""
    return [int(text) if text.isdigit() else text for text in s.replace(".ts", "").split("_")]

def create_concat_file(OUTPUT_DIR):
    """Create a properly formatted file_list.txt with numerically sorted .ts files."""
    concat_file = os.path.join(OUTPUT_DIR, "file_list.txt")

    ts_files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".ts")]
    ts_files.sort(key=natural_sort_key)  # Sort numerically sudo apt install ffmpeg  

    with open(concat_file, "w") as f:
        for ts_file in ts_files:
            f.write(f"file '{ts_file}'\n")

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
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found!")
        return

    process = (
    ffmpeg.input(input_file)
    .output(output_file,
    #  vcodec="libx264", crf=23, preset="fast", acodec="aac", **{"b:a": "128k"}
            vcodec="libx265", 
            crf=32, 
            preset="slow",  
            vf="scale=1280:720", 
            r=24,  
            acodec="aac", 
            audio_bitrate="64k"  
     
     )
    .global_args("-progress", "pipe:1", "-nostats")  
    .run_async(pipe_stdout=True, pipe_stderr=True))

    while True:
        line = process.stdout.readline().decode("utf-8", errors="ignore")
        if not line:
            break
        if "out_time_ms" in line:  
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

        fragment_count = d.split("/")[-1:][0].split(".")[0]

        
        me = await client.get_me()
        bot_username = me.username

        OUTPUT_DIR = f"{bot_username}_ts_files"  
        OUTPUT_VIDEO = f"{bot_username}_output.mp4" 
        COMPRESSED_VIDEO = f"{bot_username}_compressed.mp4"
        
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        await message.reply_text("Starting video download and processing...")

        logging.info(f" total segment : {fragment_count}")

        ts_files = download_all_ts_files(BASE_URL, int(fragment_count), OUTPUT_DIR)
        await message.reply_text("All .ts files downloaded. merging the video....")

        # Step 2: Merge .ts files
        merge_ts_files(OUTPUT_DIR, OUTPUT_VIDEO)
        await message.reply_text("Video merged. compressing video....")
 
        # Step 3: Compress the video
        # compress_video(OUTPUT_VIDEO, COMPRESSED_VIDEO)
        await message.reply("taking ss...")
        ts_to_image(OUTPUT_VIDEO, "frame.jpg", "00:00:05")
        await message.reply_text("Video compressed.")

        # Step 4: Upload the video to Telegram
        await message.reply("uploading video")
        await client.send_video(chat_id=message.chat.id, video=OUTPUT_VIDEO, caption="Here's your compressed video!", thumb="frame.jpg", width=640, height=360, supports_streaming=True)
        await message.reply("uploaded video")


        if os.path.exists(OUTPUT_VIDEO):
            os.remove(OUTPUT_VIDEO)

        if os.path.exists("frame.jpg"):
            os.remove("frame.jpg")

        if os.path.exists(COMPRESSED_VIDEO):
            os.remove(COMPRESSED_VIDEO)
            
        if os.path.exists(OUTPUT_DIR):
                for ts_file in ts_files:
                    try:
                        os.remove(ts_file)
                    except Exception as e:
                        print(f"got error in deleting {ts_file}")

        if os.path.exists(f"{OUTPUT_DIR}/file_list.txt"):
            os.remove(f"{OUTPUT_DIR}/file_list.txt")


    except Exception as e:
        await message.reply(f" Got error in this command : {e}")


@Client.on_message(filters.command("video"))
async def send_video(client: Client, message: Message):
    await message.reply("sending video...")
    ts_to_image("manhwa_robot_output.mp4", "frame.jpg", "00:00:05")
    await client.send_animation(chat_id=message.chat.id, animation="manhwa_robot_output.mp4", caption="Here's your compressed video", thumb="frame.jpg", width=640, height=360)

 
@Client.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    await message.reply(f"i am online")

