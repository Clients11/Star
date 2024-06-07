import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
from DAXXMUSIC import app


approved_cards = []
declined_cards = []
invalid_format_cards = []
user_id = None

@app.on_message(filters.document)
async def handle_document(client, message):
    global approved_cards, declined_cards, invalid_format_cards, user_id
    approved_cards = []
    declined_cards = []
    invalid_format_cards = []
    user_id = message.from_user.id

    document = message.document
    if document.mime_type == 'text/plain':
        await message.download(f"/tmp/{document.file_name}")
        
        with open(f"/tmp/{document.file_name}", 'r') as file:
            card_details = file.readlines()
        
        for line in card_details:
            parts = line.strip().split('|')
            if len(parts) == 4:
                card_number, exp_month, exp_year, cvc = parts
                is_approved = random.random() < 0.2  # 20% chance of approval
                if is_approved:
                    response_type = random.choice([
                        "Approved\nPayment Completed", 
                        "Approved\nInsufficient Funds", 
                        "CVV LIVE", 
                        "Your card's security code is invalid.",
                        "succeeded | CCN CHARGED = 1.25$ ✅"
                    ])
                    result = (
                        f"𝗖𝗮𝗿𝗱: {card_number}|{exp_month}|{exp_year}|{cvc}\n"
                        f"𝐆𝐚𝐭𝐞𝐰𝐚𝐲: Braintree Auth\n"
                        f"𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: {response_type}"
                    )
                    approved_cards.append(f"𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅\n{result}")
                else:
                    result = (
                        f"𝗖𝗮𝗿𝗱: {card_number}|{exp_month}|{exp_year}|{cvc}\n"
                        f"𝐆𝐚𝐭𝐞𝐰𝐚𝐲: Braintree Auth\n"
                        f"𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: Card Issuer Declined CVV"
                    )
                    declined_cards.append(f"𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌\n{result}")
                await message.reply(f"Checking card {i+1}/{total_cards}\n{result}")
                await asyncio.sleep(random.uniform(2, 4))  # Simulate realistic processing time
            else:
                invalid_format_cards.append(line.strip())
        
        total_cards = len(card_details)
        approved_count = len(approved_cards)
        declined_count = len(declined_cards)
        invalid_count = len(invalid_format_cards)

        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(f"View Approved Cards ({approved_count})", callback_data="view_approved")],
                [InlineKeyboardButton(f"View Declined Cards ({declined_count})", callback_data="view_declined")]
            ]
        )

        await message.reply(
            f"Processing Complete!\nTotal Cards: {total_cards}\nApproved: {approved_count}\nDeclined: {declined_count}\nInvalid Format: {invalid_count}",
            reply_markup=keyboard
        )
    else:
        await message.reply("Please upload a valid .txt file.")

@app.on_callback_query(filters.regex("view_approved"))
async def view_approved(client, callback_query):
    if callback_query.from_user.id != user_id:
        await callback_query.answer("You are not authorized to view these results.", show_alert=True)
        return
    global approved_cards
    if approved_cards:
        approved_text = "\n\n".join(approved_cards)
        approved_cards = []  # Clear approved cards after displaying
        await callback_query.message.reply(f"Approved Cards:\n{approved_text}")
    else:
        await callback_query.message.reply("No approved cards.")
    await update_buttons(callback_query)

@app.on_callback_query(filters.regex("view_declined"))
async def view_declined(client, callback_query):
    if callback_query.from_user.id != user_id:
        await callback_query.answer("You are not authorized to view these results.", show_alert=True)
        return
    global declined_cards
    if declined_cards:
        declined_text = "\n\n".join(declined_cards)
        declined_cards = []  # Clear declined cards after displaying
        await callback_query.message.reply(f"Declined Cards:\n{declined_text}")
    else:
        await callback_query.message.reply("No declined cards.")
    await update_buttons(callback_query)

async def update_buttons(callback_query):
    global approved_cards, declined_cards
    approved_count = len(approved_cards)
    declined_count = len(declined_cards)
    
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(f"View Approved Cards ({approved_count})", callback_data="view_approved")],
            [InlineKeyboardButton(f"View Declined Cards ({declined_count})", callback_data="view_declined")]
        ]
    )
    
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)
    await callback_query.answer()
