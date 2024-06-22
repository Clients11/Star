import os
import instaloader
from pyrogram import Client, filters
from DAXXMUSIC import app


app = Client("instagram_reels_bot")

# Initialize Instaloader
loader = instaloader.Instaloader()


@app.on_message(filters.text & ~filters.command("insta"))
def download_reel(client, message):
    url = message.text

    if "instagram.com/reel/" in url:
        try:
            # Extract shortcode from URL
            shortcode = url.split("/reel/")[1].split("/")[0]
            
            # Download the reel
            loader.download_post(instaloader.Post.from_shortcode(loader.context, shortcode), target=".")

            # Find the downloaded file (it should be the only .mp4 file in the directory)
            video_file = None
            for file in os.listdir("."):
                if file.endswith(".mp4"):
                    video_file = file
                    break

            if video_file:
                message.reply_video(video_file)
                os.remove(video_file)
            else:
                message.reply("Failed to find the downloaded video.")
        except Exception as e:
            message.reply(f"An error occurred: {e}")
    else:
        message.reply("Please send a valid Instagram Reel URL.")
