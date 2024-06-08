from pyrogram import Client, filters
from pathlib import Path
from DAXXMUSIC import app as bot
from DAXXMUSIC import app as user

@bot.on_message(filters.command('scr'))
async def cmd_scr(client, message):
    msg = message.text[len('/scr '):]
    splitter = msg.split(' ')
    if len(msg) == 0:
        resp = f"""
𝗪𝗿𝗼𝗻𝗴 𝗙𝗼𝗿𝗺𝗮𝘁 ❌

𝗨𝘀𝗮𝗴𝗲:
𝗙𝗼𝗿 𝗣𝘂𝗯𝗹𝗶𝗰 𝗚𝗿𝗼𝘂𝗽 𝗦𝗰𝗿𝗮𝗽𝗽𝗶𝗻𝗴
<code>/scr username 50</code>

𝗙𝗼𝗿 𝗣𝗿𝗶𝘃𝗮𝘁𝗲 𝗚𝗿𝗼𝘂𝗽 𝗦𝗰𝗿𝗮𝗽𝗽𝗶𝗻𝗴
<code>/scr https://t.me/+aGWRGz 50</code>
        """
        await message.reply_text(resp, message.id)
    else:
        user_id = str(message.from_user.id)
        chat_type = str(message.chat.type)
        chat_id = str(message.chat.id)
        
        try:
            limit = int(splitter[1])
        except:
            limit = 100

        delete = await message.reply_text("𝗦𝗰𝗿𝗮𝗽𝗶𝗻𝗴 𝗪𝗮𝗶𝘁...", message.id)
        channel_link = splitter[0]
        if "https" in channel_link:
            try:
                join = await user.join_chat(channel_link)
                title = join.title
                channel_id = join.id
                amt_cc = 0
                dublicate = 0
                async for msg in user.get_chat_history(channel_id, limit):
                    all_history = str(msg.text)
                    if all_history == 'None':
                        all_history = "INVALID CC NUMBER BC"
                    else:
                        all_history = all_history
                    all_cards = all_history.split('\n')
                    cards = []
                    for x in all_cards:
                        car = getcards(x)
                        if car:
                            cards.append(car)
                        else:
                            continue
                    len_cards = len(cards)
                    if not len_cards:
                        resp = "𝗡𝗢𝗧 𝗙𝗢𝗨𝗡𝗗 𝗔𝗡𝗬 𝗩𝗔𝗟𝗜𝗗 𝗖𝗔𝗥𝗗"
                    for item in cards:
                        amt_cc += 1
                        cc = item[0]
                        mes = item[1]
                        ano = item[2]
                        cvv = item[3]
                        fullcc = f"{cc}|{mes}|{ano}|{cvv}"

                        file_name = f"{limit}x_CC_Scraped_By_@AnzooBot.txt"
                        with open(file_name, 'a') as f:
                            cclist = open(f"{file_name}").read().splitlines()
                            if fullcc in cclist:
                                dublicate += 1
                            else:
                                f.write(f"{fullcc}\n")

                total_cc = amt_cc
                cc_found = total_cc - dublicate
                await bot.delete_messages(message.chat.id, delete.id)
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
                    reply_to_message_id=message.id)

                if scr_done:
                    name = document
                    my_file = Path(name)
                    my_file.unlink(missing_ok=True)

            except Exception as e:
                e = str(e)
                fr_error = 'Telegram says: [400 USER_ALREADY_PARTICIPANT] - The user is already a participant of this chat (caused by "messages.ImportChatInvite")'
                sec_error = 'Telegram says: [400 INVITE_HASH_EXPIRED] - The chat invite link is no longer valid (caused by "messages.ImportChatInvite")'
                if e == fr_error:
                    chat_info = await user.get_chat(channel_link)
                    channel_id = chat_info.id
                    title = chat_info.title
                    try:
                        amt_cc = 0
                        dublicate = 0
                        async for msg in user.get_chat_history(channel_id, limit):
                            all_history = str(msg.text)
                            if all_history == 'None':
                                all_history = "INVALID CC NUMBER BC"
                            else:
                                all_history = all_history
                            all_cards = all_history.split('\n')
                            cards = []
                            for x in all_cards:
                                car = getcards(x)
                                if car:
                                    cards.append(car)
                                else:
                                    continue
                            len_cards = len(cards)
                            if not len_cards:
                                resp = "𝗡𝗢𝗧 𝗙𝗢𝗨𝗡𝗗 𝗔𝗡𝗬 𝗩𝗔𝗟𝗜𝗗 𝗖𝗔𝗥𝗗"
                            for item in cards:
                                amt_cc += 1
                                cc = item[0]
                                mes = item[1]
                                ano = item[2]
                                cvv = item[3]
                                fullcc = f"{cc}|{mes}|{ano}|{cvv}"

                                file_name = f"{limit}x_CC_Scraped_By_@AnzooBot.txt"
                                with open(file_name, 'a') as f:
                                    cclist = open(f"{file_name}").read().splitlines()
                                    if fullcc in cclist:
                                        dublicate += 1
                                    else:
                                        f.write(f"{fullcc}\n")

                        total_cc = amt_cc
                        cc_found = total_cc - dublicate
                        await bot.delete_messages(message.chat.id, delete.id)
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
                            reply_to_message_id=message.id)

                        if scr_done:
                            name = document
                            my_file = Path(name)
                            my_file.unlink(missing_ok=True)

                    except Exception as e:
                        await message.reply_text(f"An error occurred: {e}", message.id)
                else:
                    await message.reply_text(f"An error occurred: {e}", message.id)
        else:
            await message.reply_text("Invalid channel link format. Please provide a valid link.", message.id)
