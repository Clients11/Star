import asyncio
from pyrogram import Client, filters, enums
import re
from pathlib import Path
from DAXXMUSIC import app, userbot
from DAXXMUSIC.core.userbot import assistants


def getcards(text: str):
    text = text.replace('\n', ' ').replace('\r', '')
    card = re.findall(r"[0-9]+", text)
    if not card or len(card) < 3:
        return

    if len(card) == 3:
        cc, mes_ano, cvv = card
        if len(mes_ano) == 3:
            mes, ano = mes_ano[:2], mes_ano[2:]
        else:
            mes, ano = mes_ano[:2], mes_ano[2:]
    elif len(card) > 3:
        cc, mes, ano, cvv = card[:4]
        if len(mes) != 2 or not ('01' <= mes <= '12'):
            mes, ano = ano, mes

    if not (cc.startswith(('3', '4', '5', '6')) and (len(cc) in [15, 16])):
        return
    if len(mes) != 2 or not ('01' <= mes <= '12'):
        return
    if len(ano) not in [2, 4] or (len(ano) == 2 and not ('21' <= ano <= '39')) or (len(ano) == 4 and not ('2021' <= ano <= '2039')):
        return
    if cc.startswith('3') and len(cvv) != 4 or len(cvv) != 3:
        return
    
    return cc, mes, ano, cvv

@app.on_message(filters.command('scr'))
async def cmd_scr(client, message):
    msg = message.text[len('/scr '):].strip()
    splitter = msg.split(' ')
    
    if not msg or len(splitter) < 2:
        resp = """
𝗪𝗿𝗼𝗻𝗴 𝗙𝗼𝗿𝗺𝗮𝘁 ❌

𝗨𝘀𝗮𝗴𝗲:
𝗙𝗼𝗿 𝗣𝘂𝗯𝗹𝗶𝗰 𝗚𝗿𝗼𝘂𝗽 𝗦𝗰𝗿𝗮𝗽𝗽𝗶𝗻𝗴
<code>/scr username 50</code>

𝗙𝗼𝗿 𝗣𝗿𝗶𝘃𝗮𝘁𝗲 𝗚𝗿𝗼𝘂𝗽 𝗦𝗰𝗿𝗮𝗽𝗽𝗶𝗻𝗴
<code>/scr https://t.me/+aGWRGz 50</code>
        """
        await message.reply_text(resp, message.id)
        return

    try:
        limit = int(splitter[1])
    except ValueError:
        limit = 100

    delete = await message.reply_text("𝗦𝗰𝗿𝗮𝗽𝗶𝗻𝗴 𝗪𝗮𝗶𝘁...", message.id)
    channel_link = splitter[0]
    
    async def scrape_channel(channel_id, limit, title):
        amt_cc = 0
        dublicate = 0
        for msg in await user.get_chat_history(channel_id, limit):
            all_history = msg.text or "INVALID CC NUMBER BC"
            all_cards = all_history.split('\n')
            cards = [getcards(x) for x in all_cards if getcards(x)]
            
            if not cards:
                continue
            
            file_name = f"{limit}x_CC_Scraped_By_@Anzooapp.txt"
            for item in cards:
                amt_cc += 1
                cc, mes, ano, cvv = item
                fullcc = f"{cc}|{mes}|{ano}|{cvv}"
                
                with open(file_name, 'a') as f:
                    cclist = f.read().splitlines()
                    if fullcc in cclist:
                        dublicate += 1
                    else:
                        f.write(f"{fullcc}\n")

        total_cc = amt_cc
        cc_found = total_cc - dublicate
        await app.delete_messages(message.chat.id, delete.id)
        caption = f"""
𝗖𝗖 𝗦𝗰𝗿𝗮𝗽𝗲𝗱 ✅

● 𝗦𝗼𝘂𝗿𝗰𝗲: {title}
● 𝗧𝗮𝗿𝗴𝗲𝘁𝗲𝗱 𝗔𝗺𝗼𝘂𝗻𝘁: {limit}
● 𝗖𝗖 𝗙𝗼𝘂𝗻𝗱: {cc_found}
● 𝗗𝘂𝗽𝗹𝗶𝗰𝗮𝘁𝗲 𝗥𝗲𝗺𝗼𝘃𝗲𝗱: {dublicate}
● 𝗦𝗰𝗿𝗮𝗽𝗲𝗱 𝗕𝘆: <a href="tg://user?id={message.from_user.id}"> {message.from_user.first_name}</a> ♻️
"""
        document = file_name
        scr_done = await message.reply_document(
            document=document,
            caption=caption,
            reply_to_message_id=message.id
        )

        if scr_done:
            Path(file_name).unlink(missing_ok=True)

    try:
        user = userbot.one
        if "https" in channel_link:
            join = await user.join_chat(channel_link)
            await scrape_channel(join.id, limit, join.title)
        else:
            chat_info = await user.get_chat(channel_link)
            await scrape_channel(chat_info.id, limit, chat_info.title)
    except Exception as e:
        error_message = str(e)
        if '[400 USER_ALREADY_PARTICIPANT]' in error_message:
            chat_info = await user.get_chat(channel_link)
            await scrape_channel(chat_info.id, limit, chat_info.title)
        else:
            await message.reply_text(f"An error occurred: {error_message}", message.id)
