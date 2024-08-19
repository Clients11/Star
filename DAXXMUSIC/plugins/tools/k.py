import json
import os
import time
import aiohttp
import asyncio
from DAXXMUSIC import app
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait

def get_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f"{int(minutes)} minutes {int(seconds)} seconds"

async def khan_data(session, message, t, headers):
    global v_count, p_count
    v_count = 0
    p_count = 0
    
    full = ""
    try:
        url = "https://khanglobalstudies.com/api/lessons/" + t 
        async with session.get(url, headers=headers) as response:
            data = await response.json()        
            videos = data.get('videos', [])
            for video in videos: 
                class_title = video.get('name')
                class_url = video.get('video_url')
                full += f"{class_title}: {class_url}\n"

                if f"{class_url}".endswith('.pdf'):
                    p_count += 1
                else:
                    v_count += 1  
                
                if video.get('pdfs', []):
                    for pdf in video['pdfs']:
                        p_count += 1
                        pdf_title = pdf.get('title')
                        pdf_url = pdf.get('url')
                        full += f"{pdf_title}: {pdf_url}\n"
            return full

    except Exception as e:
        await message.reply_text(str(e))

@app.on_message(filters.command("khan"))
async def khan_command_handler(client: Client, message: Message):
    global v_count, p_count
    msg = await message.reply_text("**🔑 For access, please transmit your ID & Password in the correct sequence:\n\n🔒 Send like this: ID*Password**")
    input1 = await client.listen(user_id=message.from_user.id)
    raw_text = input1.text
    
    login_url = "https://khanglobalstudies.com/api/login-with-password"

    headers = {
        "Host": "khanglobalstudies.com",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "okhttp/3.9.1"
    }
    data = {
        "password": "",
        "phone": ""
    }
    data["phone"] = raw_text.split("*")[0]
    data["password"] = raw_text.split("*")[1]
    await input1.delete(True)

    async with aiohttp.ClientSession() as session:
        async with session.post(login_url, headers=headers, data=data) as response:
            if response.status == 200:
                data = await response.json()
                token = data.get("token")  
                if token:
                    await msg.edit_text("✅ Login Successful") 
                else:
                    await msg.edit_text("Login failed: Token not found in response")
                    return
            else:
                await msg.edit_text("Login failed")
                return

        if token:
            headers = {
                "Host": "khanglobalstudies.com",
                "authorization": f"Bearer {token}",
                "accept-encoding": "gzip",
                "user-agent": "okhttp/3.9.1"
            }
        else:
            return await msg.edit_text("Failed to get token")

        course_url = "https://khanglobalstudies.com/api/user/v2/courses"
        async with session.get(course_url, headers=headers) as response:
            data = await response.json()

        FFF = "**BATCH-ID   -   BATCH-NAME**\n\n"
        for course in data:
            FFF += f"`{course['id']}`   -   **{course['title']}**\n\n"

        await msg.edit_text(f"{FFF}\n\n**Now send the Batch ID to Download**")
        input3 = await client.listen(user_id=message.from_user.id)
        await input3.delete(True)
        raw_text3 = input3.text
        for course in data:
            if int(course['id']) == int(raw_text3):
                batch_name = course['title'].replace('/', '')
                break
            else:
                batch_name = "KHAN-SIR"
                    
        url = f"https://khanglobalstudies.com/api/user/courses/{raw_text3}/v2-lessons"
        async with session.get(url, headers=headers) as response:
            data = await response.json()

        await msg.edit_text("**Extracting Videos Links Please Wait  📥**")
        start_time = time.time()
        vt = ""
        tasks = [khan_data(session, message, str(data['id']), headers) for data in data]
        results = await asyncio.gather(*tasks)
        for result in results:
            vt += result

        end_time = time.time()
        duration_seconds = end_time - start_time
        elapsed = get_time(duration_seconds)

        with open(f"{batch_name}.txt", 'a') as f:
            f.write(vt)
        
        c_txt = f"**App Name: Khan-Sir\nBatch Name:** `{batch_name}`\n\n🍿 **Total Video**: `{v_count}`\n📝 **Total pdf**: `{p_count}`\n⌚️**Time Taken**: `{elapsed}`"
        await message.reply_document(document=f"{batch_name}.txt", caption=c_txt)
        await msg.delete()
        os.remove(f"{batch_name}.txt")

