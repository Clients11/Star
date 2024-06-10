import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
from DAXXMUSIC import app

approved_cards = []
declined_cards = []
invalid_format_cards = []

@app.on_message(filters.document)
async def handle_document(client, message):
    global approved_cards, declined_cards, invalid_format_cards
    approved_cards = []
    declined_cards = []
    invalid_format_cards = []

    document = message.document
    if document.mime_type == 'text/plain':
        await message.download(f"/tmp/{document.file_name}")
        
        with open(f"/tmp/{document.file_name}", 'r') as file:
            card_details = file.readlines()
        
        for line in card_details:
            parts = line.strip().split('|')
            if len(parts) == 4:
                card_number, exp_month, exp_year, cvc = parts
                is_approved = random.random() < 0.01  # 1% chance of approval
                if is_approved:
                    response = 'Payment method successfully added.'
                else:
                    response = random.choice(['Card Issuer Declined CVV', 'Insufficient Funds', 'street address.', 'Gateway Rejected: avs', 'Status code avs: Gateway Rejected: avs', 'payment method added:', 'Duplicate card exists in the vault.', 'woocommerce-message'])

                if 'Card Issuer Declined CVV' in response:
                    result = f"𝗖𝗮𝗿𝗱: {card_number}|{exp_month}|{exp_year}|{cvc}\n𝐆𝐚𝐭𝐞𝐰𝐚𝐲: Braintree Auth\n𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: Declined CVV ❎"
                    declined_cards.append(f"Declined CVV ❎\n{result}")
                elif 'Insufficient Funds' in response:
                    result = f"𝗖𝗮𝗿𝗱: {card_number}|{exp_month}|{exp_year}|{cvc}\n𝐆𝐚𝐭𝐞𝐰𝐚𝐲: Braintree Auth\n𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: Insufficient Funds. ✅"
                    declined_cards.append(f"Insufficient Funds. ✅\n{result}")
                elif any(keyword in response for keyword in ['Payment method successfully added.', 'street address.', 'Gateway Rejected: avs', 'Status code avs: Gateway Rejected: avs', 'payment method added:', 'Duplicate card exists in the vault.', 'woocommerce-message']):
                    result = f"𝗖𝗮𝗿𝗱: {card_number}|{exp_month}|{exp_year}|{cvc}\n𝐆𝐚𝐭𝐞𝐰𝐚𝐲: Braintree Auth\n𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: Approved ✅"
                    approved_cards.append(f"Approved ✅\n{result}")
            else:
                invalid_format_cards.append(line.strip())
        
        total_cards = len(card_details)
        approved_count = len(approved_cards)
        declined_count = len(declined_cards)
        invalid_count = len(invalid_format_cards)

        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(f"𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅ ({approved_count})", callback_data="view_approved")],
                [InlineKeyboardButton(f"𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌ ({declined_count})", callback_data="view_declined")],
                [InlineKeyboardButton(f"𝐈𝐧𝐯𝐚𝐥𝐢𝐝👽 ({invalid_count})", callback_data="view_invalid")],
            ]
        )

        await message.reply(
            f"𝘚𝘏𝘖𝘗𝘐𝘍𝘠 + 𝘈𝘜𝘛𝘏𝘖𝘙𝘐𝘡𝘌 $5!\n \n 𝐓𝐨𝐭𝐚𝐥 𝐂𝐚𝐫𝐝𝐬 💳: {total_cards}\n 𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅: {approved_count}\n𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌: {declined_count}\n 𝐈𝐧𝐯𝐚𝐥𝐢𝐝👽 : {invalid_count}",
            reply_markup=keyboard
        )
    else:
        await message.reply("Please upload a valid .txt file.")

@app.on_callback_query(filters.regex("view_approved"))
async def view_approved(client, callback_query):
    global approved_cards
    if approved_cards:
        approved_text = "\n\n".join(approved_cards)
        approved_cards = []  # Clear approved cards after displaying
        await callback_query.message.reply(f"𝖦𝖠𝖳𝖤𝖶𝖠𝖸: 𝖲𝖧𝖮𝖯𝖨𝖥𝖸 + 𝖠𝖴𝖳𝖧𝖮𝖱𝖨𝖹𝖤 $5:\n\n{approved_text}")
    else:
        await callback_query.message.reply("No approved cards.")
    await update_buttons(callback_query)

@app.on_callback_query(filters.regex("view_declined"))
async def view_declined(client, callback_query):
    global declined_cards
    if declined_cards:
        declined_text = "\n\n".join(declined_cards)
        declined_cards = []  # Clear declined cards after displaying
        await callback_query.message.reply(f"Declined Cards:\n{declined_text}")
    else:
        await callback_query.message.reply("No declined cards.")
    await update_buttons(callback_query)

@app.on_callback_query(filters.regex("view_invalid"))
async def view_invalid(client, callback_query):
    global invalid_format_cards
    if invalid_format_cards:
        invalid_text = "\n".join(invalid_format_cards)
        invalid_format_cards = []  # Clear invalid format cards after displaying
        await callback_query.message.reply(f"Invalid Format Cards:\n{invalid_text}")
    else:
        await callback_query.message.reply("No invalid format cards.")
    await update_buttons(callback_query)

async def update_buttons(callback_query):
    global approved_cards, declined_cards, invalid_format_cards
    approved_count = len(approved_cards)
    declined_count = len(declined_cards)
    invalid_count = len(invalid_format_cards)
    
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(f"𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅ ({approved_count})", callback_data="view_approved")],
            [InlineKeyboardButton(f"𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌ ({declined_count})", callback_data="view_declined")],
            [InlineKeyboardButton(f"𝐈𝐧𝐯𝐚𝐥𝐢𝐝👽 ({invalid_count})", callback_data="view_invalid")],
        ]
    )
    
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)
    await callback_query.answer()
